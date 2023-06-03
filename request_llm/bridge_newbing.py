"""
==================================================== ========================
Part 1: From EdgeGPT.py
https://github.com/acheong08/EdgeGPT
==================================================== ========================
"""
from .edge_gpt import NewbingChatbot
load_message = "Waiting for NewBing to respond."

"""
==================================================== ========================
The second part: subprocess Worker (call body)
==================================================== ========================
"""
import time
import json
import re
import logging
import asyncio
import importlib
import threading
from toolbox import update_ui, get_conf, trimmed_format_exc
from multiprocessing import Process, Pipe

def preprocess_newbing_out(s):
     pattern = r'\^(\d+)\^' # match ^digits^
     sub = lambda m: '('+m.group(1)+')' # use the matched number as the replacement value
     result = re.sub(pattern, sub, s) # replace operation
     if '[1]' in result:
         result += '\n\n```reference\n' + "\n".join([r for r in result.split('\n') if r.startswith('[')]) + ' \n```\n'
     return result

def preprocess_newbing_out_simple(result):
     if '[1]' in result:
         result += '\n\n```reference\n' + "\n".join([r for r in result.split('\n') if r.startswith('[')]) + ' \n```\n'
     return result

class NewBingHandle(Process):
     def __init__(self):
         super().__init__(daemon=True)
         self. parent, self. child = Pipe()
         self. newbing_model = None
         self.info = ""
         self. success = True
         self.local_history = []
         self. check_dependency()
         self. start()
         self. threadLock = threading. Lock()
        
     def check_dependency(self):
         try:
             self. success = False
             import certifi, httpx, rich
             self.info = "Dependency detection passed, waiting for NewBing's response. Note that multiple people cannot call the NewBing interface at the same time (with thread lock), otherwise it will cause each person's NewBing query history to penetrate each other. When calling NewBing, it will automatically use the configured agent."
             self. success = True
         except:
             self.info = "Missing dependencies, if you want to use Newbing, in addition to the basic pip dependencies, you also need to run `pip install -r request_llm/requirements_newbing.txt` to install Newbing dependencies."
             self. success = False

     def ready(self):
         return self. newbing_model is not None

     async def async_run(self):
         # read configuration
         NEWBING_STYLE, = get_conf('NEWBING_STYLE')
         from request_llm.bridge_all import model_info
         endpoint = model_info['newbing']['endpoint']
         while True:
             # wait
             kwargs = self.child.recv()
             question=kwargs['query']
             history = kwargs['history']
             system_prompt = kwargs['system_prompt']

             # Whether to reset
             if len(self.local_history) > 0 and len(history)==0:
                 await self.newbing_model.reset()
                 self.local_history = []

             # start asking questions
             prompt = ""
             if system_prompt not in self.local_history:
                 self.local_history.append(system_prompt)
                 prompt += system_prompt + '\n'

             # append history
             for ab in history:
                 a, b = ab
                 if a not in self.local_history:
                     self.local_history.append(a)
                     prompt += a + '\n'
                 # if b not in self. local_history:
                 # self. local_history. append(b)
                 # prompt += b + '\n'

             # question
prompt += question
             self.local_history.append(question)
             print('question:', prompt)
             # submit
             async for final, response in self.newbing_model.ask_stream(
                 prompt=question,
                 conversation_style=NEWBING_STYLE, # ["creative", "balanced", "precise"]
                 wss_link=endpoint, # "wss://sydney.bing.com/sydney/ChatHub"
             ):
                 if not final:
                     print(response)
                     self. child. send(str(response))
                 else:
                     print('--------receive final ---------')
                     self. child. send('[Finish]')
                     # self.local_history.append(response)

    
     def run(self):
         """
         This function runs in the child process
         """
         # First run, load parameters
         self. success = False
         self.local_history = []
         if (self. newbing_model is None) or (not self. success):
             # proxy settings
             proxies, = get_conf('proxies')
             if proxies is None:
                 self.proxies_https = None
             else:
                 self.proxies_https = proxies['https']
             # cookie
             NEWBING_COOKIES, = get_conf('NEWBING_COOKIES')
             try:
                 cookies = json. loads(NEWBING_COOKIES)
             except:
                 self. success = False
                 tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
                 self.child.send(f'[Local Message] Newbing component cannot be loaded. NEWBING_COOKIES is not filled or has a wrong format.')
                 self. child. send('[Fail]')
                 self. child. send('[Finish]')
                 raise RuntimeError(f"Cannot load Newbing component. NEWBING_COOKIES is not filled or has a wrong format.")

             try:
                 self.newbing_model = NewbingChatbot(proxy=self.proxies_https, cookies=cookies)
             except:
                 self. success = False
                 tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
                 self.child.send(f'[Local Message] cannot load Newbing component.{tb_str}')
                 self. child. send('[Fail]')
                 self. child. send('[Finish]')
                 raise RuntimeError(f"Cannot load Newbing component.")

         self. success = True
         try:
             # Enter task waiting state
             asyncio. run(self. async_run())
         except Exception:
             tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
             self.child.send(f'[Local Message] Newbing failed {tb_str}.')
             self. child. send('[Fail]')
             self. child. send('[Finish]')
        
def stream_chat(self, **kwargs):
         """
         This function runs in the main process
         """
         self. threadLock. acquire()
         self.parent.send(kwargs) # Send request to child process
         while True:
             res = self.parent.recv() # Waiting for newbing to reply to the fragment
             if res == '[Finish]':
                 break # end
             elif res == '[Fail]':
                 self. success = False
                 break
             else:
                 yield res # fragment of newbing reply
         self. threadLock. release()


"""
==================================================== ========================
Part 3: The main process uniformly calls the function interface
==================================================== ========================
"""
global newbing_handle
newbing_handle = None

def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=None, console_slience=False):
     """
         multithreaded method
         For the description of the function, please see request_llm/bridge_all.py
     """
     global newbing_handle
     if (newbing_handle is None) or (not newbing_handle.success):
         newbing_handle = NewBingHandle()
         observe_window[0] = load_message + "\n\n" + newbing_handle.info
         if not newbing_handle.success:
             error = newbing_handle.info
             newbing_handle = None
             raise RuntimeError(error)

     # There is no sys_prompt interface, so add prompt to history
     history_feedin = []
     for i in range(len(history)//2):
         history_feedin.append([history[2*i], history[2*i+1]] )

     watch_dog_patience = 5 # watchdog's patience, set it to 5 seconds
     response = ""
     observe_window[0] = "[Local Message]: Waiting for NewBing response..."
     for response in newbing_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=sys_prompt, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']) :
         observe_window[0] = preprocess_newbing_out_simple(response)
         if len(observe_window) >= 2:
             if (time.time()-observe_window[1]) > watch_dog_patience:
                 raise RuntimeError("Program terminated.")
     return preprocess_newbing_out_simple(response)

def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
     """
         single thread method
         For the description of the function, please see request_llm/bridge_all.py
     """
     chatbot.append((inputs, "[Local Message]: Waiting for NewBing response..."))

     global newbing_handle
     if (newbing_handle is None) or (not newbing_handle.success):
         newbing_handle = NewBingHandle()
         chatbot[-1] = (inputs, load_message + "\n\n" + newbing_handle.info)
         yield from update_ui(chatbot=chatbot, history=[])
         if not newbing_handle.success:
             newbing_handle = None
             return
        
if additional_fn is not None:
         import core_functional
         importlib.reload(core_functional) # hot update prompt
         core_functional = core_functional. get_core_functions()
         if "PreProcess" in core_functional[additional_fn]: inputs = core_functional[additional_fn]["PreProcess"](inputs) # Get the preprocessing function (if any)
         inputs = core_functional[additional_fn]["Prefix"] + inputs + core_functional[additional_fn]["Suffix"]

     history_feedin = []
     for i in range(len(history)//2):
         history_feedin.append([history[2*i], history[2*i+1]] )

     chatbot[-1] = (inputs, "[Local Message]: Waiting for NewBing response...")
     response = "[Local Message]: Waiting for NewBing response..."
     yield from update_ui(chatbot=chatbot, history=history, msg="NewBing responds slowly and has not completed all responses. Please be patient before submitting a new question.")
     for response in newbing_handle.stream_chat(query=inputs, history=history_feedin, system_prompt=system_prompt, max_length=llm_kwargs['max_length'], top_p=llm_kwargs['top_p'], temperature=llm_kwargs['temperature']) :
         chatbot[-1] = (inputs, preprocess_newbing_out(response))
         yield from update_ui(chatbot=chatbot, history=history, msg="NewBing responds slowly and has not completed all responses. Please be patient before submitting a new question.")
     if response == "[Local Message]: Waiting for NewBing's response...": response = "[Local Message]: NewBing's response is abnormal, please refresh the interface and try again..."
     history. extend([inputs, response])
     logging. info(f'[raw_input] {inputs}')
     logging. info(f'[response] {response}')
     yield from update_ui(chatbot=chatbot, history=history, msg="Complete all responses, please submit a new question.")
