from .bridge_newbing import preprocess_newbing_out, preprocess_newbing_out_simple
from multiprocessing import Process, Pipe
from toolbox import update_ui, get_conf, trimmed_format_exc
import threading
import importlib
import logging
import time
from toolbox import get_conf
import asyncio
load_message = "Loading Claude components, please wait..."

try:
     """
     ==================================================== ========================
     Part 1: Slack API Client
     https://github.com/yokonsan/claude-in-slack-api
     ==================================================== ========================
     """

     from slack_sdk.errors import SlackApiError
     from slack_sdk.web.async_client import AsyncWebClient

     class SlackClient(AsyncWebClient):
         """The SlackClient class is used to interact with the Slack API to implement functions such as message sending and receiving.

             Attributes:
             - CHANNEL_ID: str type, indicating the channel ID.

             method:
             - open_channel(): an asynchronous method. Open a channel by calling the conversations_open method and store the returned channel ID in the attribute CHANNEL_ID.
             - chat(text: str): an asynchronous method. Send a text message to an already opened channel.
             - get_slack_messages(): asynchronous method. Get the latest news of the opened channel and return the message list, currently does not support historical message query.
             - get_reply(): asynchronous method. Loop to monitor the messages of the opened channel, if you receive a message ending with "Typing…_", it means that Claude is still outputting, otherwise end the loop.

         """
         CHANNEL_ID = None

         async def open_channel(self):
             response = await self.conversations_open(users=get_conf('SLACK_CLAUDE_BOT_ID')[0])
             self.CHANNEL_ID = response["channel"]["id"]

         async def chat(self, text):
             if not self.CHANNEL_ID:
                 raise Exception("Channel not found.")

             resp = await self.chat_postMessage(channel=self.CHANNEL_ID, text=text)
             self.LAST_TS = resp["ts"]

         async def get_slack_messages(self):
             try:
                 # TODO: Historical messages are not supported temporarily, because there is a problem of historical message penetration when multiple people use the same channel
                 resp = await self.conversations_history(channel=self.CHANNEL_ID, oldest=self.LAST_TS, limit=1)
                 msg = [msg for msg in resp["messages"]
                     if msg.get("user") == get_conf('SLACK_CLAUDE_BOT_ID')[0]]
                 return msg
             except (SlackApiError, KeyError) as e:
                 raise RuntimeError(f"Failed to get Slack message.")
        
         async def get_reply(self):
             while True:
                 slack_msgs = await self. get_slack_messages()
                 if len(slack_msgs) == 0:
                     await asyncio. sleep(0.5)
                     continue
                
                 msg = slack_msgs[-1]
                 if msg["text"].endswith("Typing…_"):
                     yield False, msg["text"]
                 else:
                     yield True, msg["text"]
                     break
except:
     pass

"""
==================================================== ========================
The second part: subprocess Worker (call body)
==================================================== ========================
"""


class ClaudeHandle(Process):
     def __init__(self):
         super().__init__(daemon=True)
         self. parent, self. child = Pipe()
         self.claude_model = None
         self.info = ""
         self. success = True
         self.local_history = []
         self. check_dependency()
         if self. success:
             self. start()
             self. threadLock = threading. Lock()

     def check_dependency(self):
         try:
             self. success = False
             import slack_sdk
             self.info = "Dependency detection passed, waiting for Claude's response. Note that at present, multiple people cannot call the Claude interface at the same time (with thread lock), otherwise it will cause everyone's Claude inquiry history to penetrate each other. When calling Claude, it will automatically use the configured agent."
             self. success = True
         except:
             self.info = "Missing dependencies, if you want to use Claude, in addition to the basic pip dependencies, you also need to run `pip install -r request_llm/requirements_slackclaude.txt` to install Claude's dependencies, and then restart the program."
             self. success = False

     def ready(self):
         return self.claude_model is not None
    
     async def async_run(self):
         await self.claude_model.open_channel()
         while True:
             # wait
             kwargs = self.child.recv()
             question = kwargs['query']
             history = kwargs['history']

             # start asking questions
             prompt = ""

             # question
             prompt += question
             print('question:', prompt)

             # submit
             await self.claude_model.chat(prompt)
            
             # get reply
             async for final, response in self.claude_model.get_reply():
                 if not final:
                     print(response)
                     self. child. send(str(response))
                 else:
                     # Prevent losing the last message
                     slack_msgs = await self.claude_model.get_slack_messages()
                     last_msg = slack_msgs[-1]["text"] if slack_msgs and len(slack_msgs) > 0 else ""
                     if last_msg:
                         self. child. send(last_msg)
                     print('--------receive final ---------')
                     self. child. send('[Finish]')
                    
     def run(self):
         """
         This function runs in the child process
         """
         # First run, load parameters
         self. success = False
         self.local_history = []
         if (self. claude_model is None) or (not self. success):
             # proxy settings
             proxies, = get_conf('proxies')
             if proxies is None:
                 self.proxies_https = None
             else:
                 self.proxies_https = proxies['https']

             try:
                 SLACK_CLAUDE_USER_TOKEN, = get_conf('SLACK_CLAUDE_USER_TOKEN')
                 self.claude_model = SlackClient(token=SLACK_CLAUDE_USER_TOKEN, proxy=self.proxies_https)
                 print('Claude component initialized successfully.')
             except:
                 self. success = False
                 tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
                 self.child.send(f'[Local Message] cannot load the Claude component. {tb_str}')
                 self. child. send('[Fail]')
                 self. child. send('[Finish]')
                 raise RuntimeError(f"Claude component cannot be loaded.")

         self. success = True
         try:
             # Enter task waiting state
             asyncio. run(self. async_run())
         except Exception:
             tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
             self.child.send(f'[Local Message] Claude failed {tb_str}.')
             self. child. send('[Fail]')
             self. child. send('[Finish]')

     def stream_chat(self, **kwargs):
         """
         This function runs in the main process
         """
         self. threadLock. acquire()
         self.parent.send(kwargs) # Send request to child process
         while True:
             res = self.parent.recv() # Waiting for Claude to reply fragment
             if res == '[Finish]':
                 break # end
             elif res == '[Fail]':
                 self. success = False
                 break
             else:
                 yield res # fragment of Claude's reply
         self. threadLock. release()

"""
==================================================== ========================
Part 3: The main process uniformly calls the function interface
==================================================== ========================
"""
global claude_handle
claude_handle = None


def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=None, console_slience=False):
     """
         multithreaded method
         For the description of the function, please see request_llm/bridge_all.py
     """
     global claude_handle
     if (claude_handle is None) or (not claude_handle.success):
         claude_handle = ClaudeHandle()
         observe_window[0] = load_message + "\n\n" + claude_handle.info
         if not claude_handle.success:
             error = claude_handle.info
             claude_handle = None
             raise RuntimeError(error)

     # There is no sys_prompt interface, so add prompt to history
     history_feedin = []
     for i in range(len(history)//2):
         history_feedin.append([history[2*i], history[2*i+1]])

     watch_dog_patience = 5 # watchdog's patience, set it to 5 seconds
     response = ""
     observe_window[0] = "[Local Message]: Waiting for Claude's response..."
     for response in claude_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=sys_prompt, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']) :
         observe_window[0] = preprocess_newbing_out_simple(response)
         if len(observe_window) >= 2:
             if (time.time()-observe_window[1]) > watch_dog_patience:
                 raise RuntimeError("Program terminated.")
     return preprocess_newbing_out_simple(response)


def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream=True, additional_fn=None):
     """
         single thread method
         For the description of the function, please see request_llm/bridge_all.py
     """
     chatbot.append((inputs, "[Local Message]: Waiting for Claude to respond..."))

     global claude_handle
     if (claude_handle is None) or (not claude_handle.success):
         claude_handle = ClaudeHandle()
         chatbot[-1] = (inputs, load_message + "\n\n" + claude_handle.info)
         yield from update_ui(chatbot=chatbot, history=[])
         if not claude_handle.success:
             claude_handle = None
             return

     if additional_fn is not None:
         import core_functional
         importlib.reload(core_functional) # hot update prompt
         core_functional = core_functional. get_core_functions()
         if "PreProcess" in core_functional[additional_fn]:
             inputs = core_functional[additional_fn]["PreProcess"](
                 inputs) # Get the preprocessing function (if any)
         inputs = core_functional[additional_fn]["Prefix"] + \
             inputs + core_functional[additional_fn]["Suffix"]

     history_feedin = []
     for i in range(len(history)//2):
         history_feedin.append([history[2*i], history[2*i+1]])

     chatbot[-1] = (inputs, "[Local Message]: Waiting for Claude to respond...")
     response = "[Local Message]: Waiting for Claude's response..."
     yield from update_ui(chatbot=chatbot, history=history, msg="Claude responds slowly and has not completed all the responses, please be patient before submitting a new question.")
     for response in claude_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=system_prompt):
         chatbot[-1] = (inputs, preprocess_newbing_out(response))
         yield from update_ui(chatbot=chatbot, history=history, msg="Claude responds slowly and has not completed all the responses, please be patient before submitting a new question.")
     if response == "[Local Message]: Waiting for Claude to respond...":
         response = "[Local Message]: Claude responded abnormally, please refresh the interface and try again..."
     history. extend([inputs, response])
     logging. info(f'[raw_input] {inputs}')
     logging. info(f'[response] {response}')
     yield from update_ui(chatbot=chatbot, history=history, msg="Complete all responses, please submit a new question.")
