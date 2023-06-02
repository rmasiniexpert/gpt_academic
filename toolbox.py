import markdown
import importlib
import traceback
import inspect
import re
import os
from latex2mathml.converter import convert as tex2mathml
from functools import wraps, lru_cache

"""
==================================================== ========================
first part
Function plug-in input and output connection area
     - ChatBotWithCookies: Chatbot class with Cookies, laying the foundation for more powerful functions
     - ArgsGeneralWrapper: Decorator function, used to reorganize input parameters, change the order and structure of input parameters
     - update_ui: refresh the interface with yield from update_ui(chatbot, history)
     - CatchException: Display all problems in the plugin on the interface
     - HotReload: Realize hot update of plugins
     - trimmed_format_exc: Print traceback, hide absolute address for security
==================================================== ========================
"""

class ChatBotWithCookies(list):
    def __init__(self, cookie):
        self._cookies = cookie

    def write_list(self, list):
        for t in list:
            self.append(t)

    def get_list(self):
        return [t for t in self]

    def get_cookies(self):
        return self._cookies


def ArgsGeneralWrapper(f):
     """
     The decorator function is used to reorganize the input parameters and change the order and structure of the input parameters.
     """
     def decorated(cookies, max_length, llm_model, txt, txt2, top_p, temperature, chatbot, history, system_prompt, plugin_advanced_arg, *args):
         txt_passon = txt
         if txt == "" and txt2 != "": txt_passon = txt2
         # Introduce a chatbot with cookies
         cookies. update({
             'top_p': top_p,
             'temperature': temperature,
         })
         llm_kwargs = {
             'api_key': cookies['api_key'],
             'llm_model': llm_model,
             'top_p': top_p,
             'max_length': max_length,
             'temperature': temperature,
         }
         plugin_kwargs = {
             "advanced_arg": plugin_advanced_arg,
         }
         chatbot_with_cookie = ChatBotWithCookies(cookies)
         chatbot_with_cookie.write_list(chatbot)
         yield from f(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, *args)
     return decorated


def update_ui(chatbot, history, msg='normal', **kwargs): # refresh interface
     """
     Refresh the UI
     """
     assert isinstance(chatbot, ChatBotWithCookies), "Don't discard the chatbot in the process of passing it. If necessary, use clear to clear it, and then use the for+append loop to reassign it."
     yield chatbot.get_cookies(), chatbot, history, msg

def trimmed_format_exc():
     import os, traceback
     str = traceback. format_exc()
     current_path = os. getcwd()
     replace_path = "."
     return str. replace(current_path, replace_path)

def CatchException(f):
     """
     Decorator function, captures the exception in function f and encapsulates it into a generator to return and display it in the chat.
     """

     @wraps(f)
     def decorated(txt, top_p, temperature, chatbot, history, systemPromptTxt, WEB_PORT=-1):
         try:
             yield from f(txt, top_p, temperature, chatbot, history, systemPromptTxt, WEB_PORT)
         except Exception as e:
             from check_proxy import check_proxy
             from toolbox import get_conf
             proxies, = get_conf('proxies')
             tb_str = '```\n' + trimmed_format_exc() + '```'
             if len(chatbot) == 0:
                 chatbot. clear()
                 chatbot.append(["plug-in scheduling exception", "abnormal reason"])
             chatbot[-1] = (chatbot[-1][0],
                            f"[Local Message] Error in experimental function call: \n\n{tb_str} \n\nCurrent proxy availability: \n\n{check_proxy(proxies)}")
             yield from update_ui(chatbot=chatbot, history=history, msg=f'abnormal {e}') # Refresh interface
     return decorated


def HotReload(f):
     """
     Decorator function of HotReload, used to implement hot update of Python function plugins.
     Function hot update refers to updating the function code without stopping the running of the program, so as to achieve real-time update function.
     Inside the decorator, wraps(f) is used to preserve the meta-information of the function, and an inner function named decorated is defined.
     The internal function reloads and obtains the function module by using the reload function of the importlib module and the getmodule function of the inspect module,
     Then get the function name through the getattr function, and reload the function in the new module.
     Finally, use the yield from statement to return the reloaded function and execute on the decorated function.
     Ultimately, the decorator function returns the inner function. This internal function can update the original definition of the function to the latest version and execute the new version of the function.
     """
     @wraps(f)
     def decorated(*args, **kwargs):
         fn_name = f.__name__
         f_hot_reload = getattr(importlib. reload(inspect. getmodule(f)), fn_name)
         yield from f_hot_reload(*args, **kwargs)
     return decorated


"""
==================================================== ========================
the second part
Other gadgets:
     - write_results_to_file: write the results to the markdown file
     - regular_txt_to_markdown: Convert normal text to Markdown formatted text.
     - report_execption: add simple unexpected error message to chatbot
     - text_divide_paragraph: Split the text according to the paragraph separator and generate HTML code with paragraph tags.
     - markdown_convertion: convert markdown into nice-looking html in a variety of ways
     - format_io: take over Gradio's default markdown processing method
     - on_file_uploaded: handle file upload (automatic decompression)
     - on_report_generated: automatically project the generated report to the file upload area
     - clip_history: Automatically truncate when the history context is too long
     - get_conf: get settings
     - select_api_key: According to the current model category, extract the available api-key
==================================================== ========================
"""

def get_reduce_token_percent(text):
     """
         * This function will be deprecated in the future
     """
     try:
         # text = "maximum context length is 4097 tokens. However, your messages resulted in 4870 tokens"
         pattern = r"(\d+)\s+tokens\b"
         match = re. findall(pattern, text)
         EXCEED_ALLO = 500 # Leave a little room, otherwise there will be problems when replying due to too little room
         max_limit = float(match[0]) - EXCEED_ALLO
         current_tokens = float(match[1])
         ratio = max_limit/current_tokens
         assert ratio > 0 and ratio < 1
         return ratio, str(int(current_tokens-max_limit))
     except:
         return 0.5, 'Unknown'


def write_results_to_file(history, file_name=None):
     """
     Write the conversation record history to a file in Markdown format. If no filename is specified, the current time is used to generate the filename.
     """
     import os
     import time
     if file_name is None:
         # file_name = time.strftime("chatGPT analysis report %Y-%m-%d-%H-%M-%S", time.localtime()) + '.md'
         file_name = 'chatGPT analysis report' + \
             time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.md'
     os.makedirs('./gpt_log/', exist_ok=True)
     with open(f'./gpt_log/{file_name}', 'w', encoding='utf8') as f:
         f.write('# chatGPT analysis report\n')
         for i, content in enumerate(history):
             try:
                 if type(content) != str: content = str(content)
             except:
                 continue
             if i % 2 == 0:
                 f.write('##')
             try:
                 f. write(content)
             except:
                 # remove everything that cannot be handled by utf8
                 f.write(content.encode('utf-8', 'ignore').decode())
             f.write('\n\n')
     res = 'The above material has been written' + os.path.abspath(f'./gpt_log/{file_name}')
     print(res)
     return res


def regular_txt_to_markdown(text):
     """
     Convert normal text to Markdown formatted text.
     """
     text = text.replace('\n', '\n\n')
     text = text.replace('\n\n\n', '\n\n')
     text = text.replace('\n\n\n', '\n\n')
     return text




def report_execption(chatbot, history, a, b):
     """
     Add error message to chatbot
     """
     chatbot. append((a, b))
     history.append(a)
     history.append(b)


def text_divide_paragraph(text):
     """
     Split the text according to paragraph delimiters and generate HTML code with paragraph tags.
     """
     if '```' in text:
         #careful input
         return text
     else:
         # wtf input
         lines = text. split("\n")
         for i, line in enumerate(lines):
             lines[i] = lines[i].replace(" ", "&nbsp;")
         text = "</br>".join(lines)
         return text

@lru_cache(maxsize=128) # Use lru cache to speed up conversion
def markdown_convertion(txt):
     """
     Convert Markdown formatted text to HTML format. If mathematical formulas are included, convert the formulas to HTML format first.
     """
     pre = '<div class="markdown-body">'
     suf = '</div>'
     if txt.startswith(pre) and txt.endswith(suf):
         # print('Warning, you have entered a converted string, there may be a problem with the second conversion')
         return txt # has already been converted, no need to convert again
    
     markdown_extension_configs = {
         'mdx_math': {
             'enable_dollar_delimiter': True,
             'use_gitlab_delimiters': False,
         },
     }
     find_equation_pattern = r'<script type="math/tex(?:.*?)>(.*?)</script>'

     def tex2mathml_catch_exception(content, *args, **kwargs):
         try:
             content = tex2mathml(content, *args, **kwargs)
         except:
             content = content
         return content

     def replace_math_no_render(match):
         content = match. group(1)
         if 'mode=display' in match.group(0):
             content = content. replace('\n', '</br>')
             return f"<font color=\"#00FF00\">$$</font><font color=\"#FF00FF\">{content}</font><font color=\"#00FF00\">$ $</font>"
         else:
             return f"<font color=\"#00FF00\">$</font><font color=\"#FF00FF\">{content}</font><font color=\"#00FF00\">$< /font>"

     def replace_math_render(match):
         content = match. group(1)
         if 'mode=display' in match.group(0):
             if '\\begin{aligned}' in content:
                 content = content.replace('\\begin{aligned}', '\\begin{array}')
                 content = content.replace('\\end{aligned}', '\\end{array}')
                 content = content. replace('&', ' ')
             content = tex2mathml_catch_exception(content, display="block")
             return content
         else:
             return tex2mathml_catch_exception(content)

     def markdown_bug_hunt(content):
         """
         Solve a mdx_math bug (additional <script> when wrapping the begin command with single $)
         """
         content = content.replace('<script type="math/tex">\n<script type="math/tex; mode=display">', '<script type="math/tex; mode=display"> ')
         content = content.replace('</script>\n</script>', '</script>')
         return content

     def no_code(txt):
         if '```' not in txt:
             return True
         else:
             if '```reference' in txt: return True # newbing
             else: return False

if ('$' in txt) and no_code(txt):  # 有$标识的公式符号，且没有代码段```的标识
        # convert everything to html format
        split = markdown.markdown(text='---')
        convert_stage_1 = markdown.markdown(text=txt, extensions=['mdx_math', 'fenced_code', 'tables', 'sane_lists'], extension_configs=markdown_extension_configs)
        convert_stage_1 = markdown_bug_hunt(convert_stage_1)
        # re.DOTALL: Make the '.' special character match any character at all, including a newline; without this flag, '.' will match anything except a newline. Corresponds to the inline flag (?s).
        # 1. convert to easy-to-copy tex (do not render math)
        convert_stage_2_1, n = re.subn(find_equation_pattern, replace_math_no_render, convert_stage_1, flags=re.DOTALL)
        # 2. convert to rendered equation
        convert_stage_2_2, n = re.subn(find_equation_pattern, replace_math_render, convert_stage_1, flags=re.DOTALL)
        # cat them together
        return pre + convert_stage_2_1 + f'{split}' + convert_stage_2_2 + suf
    else:
        return pre + markdown.markdown(txt, extensions=['fenced_code', 'codehilite', 'tables', 'sane_lists']) + suf


def close_up_code_segment_during_stream(gpt_reply):
     """
     In the middle of the gpt output code (the previous ``` is output, but the following ``` has not been output), add the following ```

     Args:
         gpt_reply (str): The reply string returned by the GPT model.

     Returns:
         str: Return a new string, which will fill in the "behind ```" of the output code fragment.

     """
     if '```' not in gpt_reply:
         return gpt_reply
     if gpt_reply.endswith('```'):
         return gpt_reply

     # Excluding the above two cases, we
     segments = gpt_reply. split('```')
     n_mark = len(segments) - 1
     if n_mark % 2 == 1:
         # print('Output code snippet!')
         return gpt_reply+'\n```'
     else:
         return gpt_reply


def format_io(self, y):
     """
     Parse input and output into HTML format. Paragraphize the input part of the last item in y and convert the Markdown and math formulas in the output part to HTML format.
     """
     if y is None or y == []:
         return []
     i_ask, gpt_reply = y[-1]
     i_ask = text_divide_paragraph(i_ask) # The input part is too free, preprocessing wave
     gpt_reply = close_up_code_segment_during_stream(gpt_reply) # When the code output half, try to make up the last ```
     y[-1] = (
         None if i_ask is None else markdown.markdown(i_ask, extensions=['fenced_code', 'tables']),
         None if gpt_reply is None else markdown_convertion(gpt_reply)
     )
     return y


def find_free_port():
     """
     Returns the unused ports available in the current system.
     """
     import socket
     from contextlib import closing
     with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
         s. bind(('', 0))
         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         return s. getsockname()[1]


def extract_archive(file_path, dest_dir):
     import zipfile
     import tarfile
     import os
     # Get the file extension of the input file
     file_extension = os.path.splitext(file_path)[1]

     # Extract the archive based on its extension
     if file_extension == '.zip':
         with zipfile.ZipFile(file_path, 'r') as zipobj:
             zipobj.extractall(path=dest_dir)
             print("Successfully extracted zip archive to {}". format(dest_dir))

     elif file_extension in ['.tar', '.gz', '.bz2']:
         with tarfile.open(file_path, 'r:*') as tarobj:
             tarobj. extractall(path=dest_dir)
             print("Successfully extracted tar archive to {}". format(dest_dir))

     # Third-party library, need pip install rarfile in advance
     # In addition, you need to install winrar software on Windows, and configure its Path environment variable, such as "C:\Program Files\WinRAR"
     elif file_extension == '.rar':
         try:
             import rarfile
             with rarfile.RarFile(file_path) as rf:
                 rf. extractall(path=dest_dir)
                 print("Successfully extracted rar archive to {}". format(dest_dir))
         except:
             print("Rar format requires additional dependencies to install")
             return '\n\n need to install pip install rarfile to decompress the rar file'

     # Third-party library, need pip install py7zr in advance
     elif file_extension == '.7z':
         try:
             import py7zr
             with py7zr.SevenZipFile(file_path, mode='r') as f:
                 f. extractall(path=dest_dir)
                 print("Successfully extracted 7z archive to {}". format(dest_dir))
         except:
             print("7z format requires additional dependencies to install")
             return '\n\n need to install pip install py7zr to decompress 7z files'
     else:
         return ''
     return ''


def find_recent_files(directory):
    """
        me: find files that is created with in one minutes under a directory with python, write a function
        gpt: here it is!
    """
    import os
    import time
    current_time = time.time()
    one_minute_ago = current_time - 60
    recent_files = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if file_path.endswith('.log'):
            continue
        created_time = os.path.getmtime(file_path)
        if created_time >= one_minute_ago:
            if os.path.isdir(file_path):
                continue
            recent_files.append(file_path)

    return recent_files


def on_file_uploaded(files, chatbot, txt, txt2, checkboxes):
     """
     Callback function when the file is uploaded
     """
     if len(files) == 0:
         return chatbot, txt
     import shut-off
     import os
     import time
     import glob
     from toolbox import extract_archive
     try:
         shutil.rmtree('./private_upload/')
     except:
         pass
     time_tag = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
     os.makedirs(f'private_upload/{time_tag}', exist_ok=True)
     err_msg = ''
     for file in files:
         file_origin_name = os.path.basename(file.orig_name)
         shutil.copy(file.name, f'private_upload/{time_tag}/{file_origin_name}')
         err_msg += extract_archive(f'private_upload/{time_tag}/{file_origin_name}',
                                    dest_dir=f'private_upload/{time_tag}/{file_origin_name}.extract')
     moved_files = [fp for fp in glob.glob('private_upload/**/*', recursive=True)]
     if "bottom input area" in checkboxes:
         txt = ""
         txt2 = f'private_upload/{time_tag}'
     else:
         txt = f'private_upload/{time_tag}'
         txt2 = ""
     moved_files_str = '\t\n\n'.join(moved_files)
     chatbot.append(['I uploaded the file, please check',
                     f'[Local Message] received the following files: \n\n{moved_files_str}' +
                     f'\n\nThe call path parameter has been automatically corrected to: \n\n{txt}' +
                     f'\n\nNow when you click any function plug-in identified by "red color", the above file will be used as input parameter'+err_msg])
     return chatbot, txt, txt2


def on_report_generated(files, chatbot):
     from toolbox import find_recent_files
     report_files = find_recent_files('gpt_log')
     if len(report_files) == 0:
         return None, chatbot
     # files. extend(report_files)
     chatbot.append(['How to obtain the report remotely?', 'The report has been added to the "file upload area" on the right (may be in a collapsed state), please check it.'])
     return report_files, chatbot

def is_openai_api_key(key):
     API_MATCH_ORIGINAL = re.match(r"sk-[a-zA-Z0-9]{48}$", key)
     API_MATCH_AZURE = re.match(r"[a-zA-Z0-9]{32}$", key)
     return bool(API_MATCH_ORIGINAL) or bool(API_MATCH_AZURE)

def is_api2d_key(key):
     if key.startswith('fk') and len(key) == 41:
         return True
     else:
         return False

def is_any_api_key(key):
     if ',' in key:
         keys = key. split(',')
         for k in keys:
             if is_any_api_key(k): return True
         return False
     else:
         return is_openai_api_key(key) or is_api2d_key(key)

def what_keys(keys):
     avail_key_list = {'OpenAI Key':0, "API2D Key":0}
     key_list = keys. split(',')

     for k in key_list:
         if is_openai_api_key(k):
             avail_key_list['OpenAI Key'] += 1

     for k in key_list:
         if is_api2d_key(k):
             avail_key_list['API2D Key'] += 1

     return f"Detected: OpenAI Key {avail_key_list['OpenAI Key']}, API2D Key {avail_key_list['API2D Key']}"

def select_api_key(keys, llm_model):
     import random
     avail_key_list = []
     key_list = keys. split(',')

     if llm_model.startswith('gpt-'):
         for k in key_list:
             if is_openai_api_key(k): avail_key_list.append(k)

     if llm_model.startswith('api2d-'):
         for k in key_list:
             if is_api2d_key(k): avail_key_list.append(k)

     if len(avail_key_list) == 0:
         raise RuntimeError(f"The api-key you provided does not meet the requirements and does not contain any api-keys available for {llm_model}. You may have selected the wrong model or request source.")

     api_key = random.choice(avail_key_list) # random load balancing
     return api_key

def read_env_variable(arg, default_value):
     """
     The environment variable can be `GPT_ACADEMIC_CONFIG` (priority), or it can be `CONFIG` directly
     For example, in windows cmd, you can write:
         set USE_PROXY=True
         set API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
         set proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
         set AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
         set AUTHENTICATION=[("username", "password"), ("username2", "password2")]
     You can also write:
         set GPT_ACADEMIC_USE_PROXY=True
         set GPT_ACADEMIC_API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
         set GPT_ACADEMIC_proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
         set GPT_ACADEMIC_AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
         set GPT_ACADEMIC_AUTHENTICATION=[("username", "password"), ("username2", "password2")]
     """
from colorful import print bright red, print bright green
     arg_with_prefix = "GPT_ACADEMIC_" + arg
     if arg_with_prefix in os.environ:
         env_arg = os.environ[arg_with_prefix]
     elif arg in os.environ:
         env_arg = os.environ[arg]
     else:
         raise KeyError
     print(f"[ENV_VAR] try to load {arg}, default value: {default_value} --> fixed value: {env_arg}")
     try:
         if isinstance(default_value, bool):
             env_arg = env_arg. strip()
             if env_arg == 'True': r = True
             elif env_arg == 'False': r = False
             else: print('enter True or False, but have:', env_arg); r = default_value
         elif isinstance(default_value, int):
             r = int(env_arg)
         elif isinstance(default_value, float):
             r = float(env_arg)
         elif isinstance(default_value, str):
             r = env_arg. strip()
         elif isinstance(default_value, dict):
             r = eval(env_arg)
         elif isinstance(default_value, list):
             r = eval(env_arg)
         elif default_value is None:
             assert arg == "proxies"
             r = eval(env_arg)
         else:
             print bright red (f"[ENV_VAR] environment variable {arg} does not support setting through environment variables! ")
             raise KeyError
     except:
         print bright red (f"[ENV_VAR] environment variable {arg} failed to load! ")
         raise KeyError(f"[ENV_VAR] environment variable {arg} failed to load! ")

     print bright green (f"[ENV_VAR] successfully read environment variable {arg}")
     return r

@lru_cache(maxsize=128)
def read_single_conf_with_lru_cache(arg):
     from colorful import print bright red, print bright green, print bright blue
     try:
         # Priority 1. Get environment variables as configuration
         default_ref = getattr(importlib.import_module('config'), arg) # read the default value as a reference for data type conversion
         r = read_env_variable(arg, default_ref)
     except:
         try:
             # Priority 2. Get the configuration in config_private
             r = getattr(importlib. import_module('config_private'), arg)
         except:
             # Priority 3. Get the configuration in config
             r = getattr(importlib. import_module('config'), arg)

     # When reading API_KEY, check if you forgot to change the config
     if arg == 'API_KEY':
         print bright blue (f"[API_KEY] This project now supports the api-keys of OpenAI and API2D. It also supports filling in multiple api-keys at the same time, such as API_KEY=\"openai-key1,openai-key2,api2d-key3\" ")
         print bright blue (f"[API_KEY] You can either modify the api-key(s) in config.py, or enter a temporary api-key(s) in the question input area, and press Enter to submit it to take effect .")
         if is_any_api_key(r):
             print bright green(f"[API_KEY] Your API_KEY is: {r[:15]}*** API_KEY imported successfully")
         else:
             print bright red ("[API_KEY] The correct API_KEY is a 51-digit key starting with 'sk' (OpenAI), or a 41-digit key starting with 'fk', please modify the API key in the config file before running." )
     if arg == 'proxies':
         if r is None:
             print bright red ('[PROXY] network proxy status: not configured. It is very likely that the model of the OpenAI family cannot be accessed in the proxyless state. Suggestion: Check whether the USE_PROXY option has been modified.')
         else:
             print bright green ('[PROXY] network proxy status: configured. The configuration information is as follows:', r)
             assert isinstance(r, dict), 'proxies format error, please pay attention to the format of the proxies option, do not miss the brackets. '
     return r


def get_conf(*args):
     # It is recommended that you copy a config_private.py to put your own secrets, such as API and proxy URL, to avoid accidentally uploading github to be seen by others
     res = []
     for arg in args:
         r = read_single_conf_with_lru_cache(arg)
         res.append(r)
     return res


def clear_line_break(txt):
     txt = txt. replace('\n', ' ')
     txt = txt. replace(' ', ' ')
     txt = txt. replace(' ', ' ')
     return txt


class DummyWith():
     """
     This code defines an empty context manager called DummyWith,
     Its function is... well... it just doesn't work, that is, it replaces other context managers without changing the code structure.
     A context manager is a Python object intended for use with the with statement,
     to ensure that some resources are properly initialized and cleaned up during code block execution.
     A context manager must implement two methods, __enter__() and __exit__().
     In the case where context execution starts, the __enter__() method is called before the code block is executed,
     At the end of context execution, the __exit__() method will be called.
     """
     def __enter__(self):
         return self

     def __exit__(self, exc_type, exc_value, traceback):
         return

def run_gradio_in_subpath(demo, auth, port, custom_path):
     """
     Change the running address of gradio to the specified secondary path
     """
     def is_path_legal(path: str)->bool:
         '''
         check path for sub url
         path: path to check
         return value: do sub url wrap
         '''
         if path == "/": return True
         if len(path) == 0:
             print("ilegal custom path: {}\npath must not be empty\ndeploy on root url".format(path))
             return False
         if path[0] == '/':
             if path[1] != '/':
                 print("deploy on sub-path {}". format(path))
                 return True
             return False
         print("ilegal custom path: {}\npath should begin with \'/\'\ndeploy on root url".format(path))
         return False

    if not is_path_legal(custom_path): raise RuntimeError('Ilegal custom path')
    import uvicorn
    import gradio as gr
    from fastapi import FastAPI
    app = FastAPI()
    if custom_path != "/":
        @app.get("/")
        def read_main(): 
            return {"message": f"Gradio is running at: {custom_path}"}
    app = gr.mount_gradio_app(app, demo, path=custom_path)
    uvicorn.run(app, host="0.0.0.0", port=port) # , auth=auth


def clip_history(inputs, history, tokenizer, max_token_limit):
     """
     reduce the length of history by clipping.
     this function search for the longest entries to clip, little by little,
     until the number of tokens of history is reduced under threshold.
     Shorten the length of the history by clipping.
     This function incrementally searches for the longest entry to clip,
     Until the number of markers recorded in the history drops below the threshold.
     """
     import numpy as np
     from request_llm.bridge_all import model_info
     def get_token_num(txt):
         return len(tokenizer. encode(txt, disallowed_special=()))
     input_token_num = get_token_num(inputs)
     if input_token_num < max_token_limit * 3 / 4:
         # When the proportion of token in the input part is less than 3/4 of the limit, when cropping
         # 1. Leave the input margin
         max_token_limit = max_token_limit - input_token_num
         # 2. Leave the margin for output
         max_token_limit = max_token_limit - 128
         # 3. If the margin is too small, clear the history directly
         if max_token_limit < 128:
             history = []
             return history
     else:
         # When the proportion of tokens in the input part > 3/4 of the limit, clear the history directly
         history = []
         return history

     everything = ['']
     everything. extend(history)
     n_token = get_token_num('\n'.join(everything))
     everything_token = [get_token_num(e) for e in everything]

     # Granularity at truncation
     delta = max(everything_token) // 16

     while n_token > max_token_limit:
         where = np.argmax(everything_token)
         encoded = tokenizer.encode(everything[where], disallowed_special=())
         clipped_encoded = encoded[:len(encoded)-delta]
         everything[where] = tokenizer.decode(clipped_encoded)[:-1] # -1 to remove the may-be illegal char
         everything_token[where] = get_token_num(everything[where])
         n_token = get_token_num('\n'.join(everything))

     history = everything[1:]
     return history
"""
==================================================== ========================
the third part
Other gadgets:
     - zip_folder: Compress all files under a certain path, and then transfer to another specified path (written by gpt)
     - gen_time_str: generate timestamp
==================================================== ========================
"""

def zip_folder(source_folder, dest_folder, zip_name):
     import zipfile
     import os
     # Make sure the source folder exists
     if not os.path.exists(source_folder):
         print(f"{source_folder} does not exist")
         return

     # Make sure the destination folder exists
     if not os.path.exists(dest_folder):
         print(f"{dest_folder} does not exist")
         return

     # Create the name for the zip file
     zip_file = os.path.join(dest_folder, zip_name)

     # Create a ZipFile object
     with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
         # Walk through the source folder and add files to the zip file
         for foldername, subfolders, filenames in os. walk(source_folder):
             for filename in filenames:
                 filepath = os.path.join(foldername, filename)
                 zipf.write(filepath, arcname=os.path.relpath(filepath, source_folder))

     # Move the zip file to the destination folder (if it wasn't already there)
     if os.path.dirname(zip_file) != dest_folder:
         os.rename(zip_file, os.path.join(dest_folder, os.path.basename(zip_file)))
         zip_file = os.path.join(dest_folder, os.path.basename(zip_file))

     print(f"Zip file created at {zip_file}")

def gen_time_str():
     import time
     return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


class ProxyNetworkActivate():
     """
     This code defines an empty context manager called TempProxy, which is used to proxy a small piece of code
     """
     def __enter__(self):
         from toolbox import get_conf
         proxies, = get_conf('proxies')
         if 'no_proxy' in os.environ: os.environ.pop('no_proxy')
         if proxies are not None:
             if 'http' in proxies: os.environ['HTTP_PROXY'] = proxies['http']
             if 'https' in proxies: os.environ['HTTPS_PROXY'] = proxies['https']
         return self

     def __exit__(self, exc_type, exc_value, traceback):
         os.environ['no_proxy'] = '*'
         if 'HTTP_PROXY' in os.environ: os.environ.pop('HTTP_PROXY')
         if 'HTTPS_PROXY' in os.environ: os.environ.pop('HTTPS_PROXY')
         return
