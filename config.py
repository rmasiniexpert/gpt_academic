# [step 1]>> For example: API_KEY = "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" (this key is invalid)
API_KEY = "sk-fill API key here" # Multiple API-KEYs can be filled in at the same time, separated by English commas, for example API_KEY = "sk-openaikey1,sk-openaikey2,fkxxxx-api2dkey1,fkxxxx-api2dkey2"

# [step 2]>> Change to True application proxy, if it is directly deployed on an overseas server, do not modify it here
USE_PROXY = False
if USE_PROXY:
     # Fill in the format is [protocol]://[address]:[port], don’t forget to change USE_PROXY to True before filling in, if you deploy directly on overseas servers, don’t modify it here
     # For example "socks5h://localhost:11284"
     # [Protocol] Common protocols are socks5h/http; for example, the default local protocol of v2**y and ss* is socks5h; and the default local protocol of cl**h is http
     # [Address] If you know everything, you can fill in localhost or 127.0.0.1 if you don’t understand. (localhost means that the agent software is installed on this machine)
     # [Port] Find it in the settings of the proxy software. Although different agent software interfaces are different, the port number should be in the most prominent position

     # The address of the proxy network, open your *learning*net software to view the proxy protocol (socks5/http), address (localhost) and port (11284)
     proxies = {
         # [protocol]://[address]:[port]
         "http": "socks5h://localhost:11284", # Another example "http": "http://127.0.0.1:7890",
         "https": "socks5h://localhost:11284", # Another example "https": "http://127.0.0.1:7890",
     }
else:
     proxies = None

# [step 3]>> In the multi-thread function plug-in, how many threads are allowed to access OpenAI at the same time by default. The limit for Free trial users is 3 times per minute, and the limit for Pay-as-you-go users is 3500 times per minute
# In a nutshell: free users fill in 3, OpenAI users with credit cards can fill in 16 or higher. Please check to increase the limit: https://platform.openai.com/docs/guides/rate-limits/overview
DEFAULT_WORKER_NUM=3


# [step 4]>> The following configuration can optimize the experience, but it does not need to be modified in most cases
# The height of the dialog window
CHATBOT_HEIGHT = 1115

# Code highlighting
CODE_HIGHLIGHT = True

# window layout
LAYOUT = "LEFT-RIGHT" # "LEFT-RIGHT" (left and right layout) # "TOP-DOWN" (top and bottom layout)
DARK_MODE = True # "LEFT-RIGHT" (left and right layout) # "TOP-DOWN" (top and bottom layout)

# After sending a request to OpenAI, how long to wait for it to be judged as timeout
TIMEOUT_SECONDS = 30

# The port of the webpage, -1 represents a random port
WEB_PORT = -1

# If OpenAI does not respond (network freeze, proxy failure, KEY failure), the number of retries is limited
MAX_RETRY = 2

# Model selection is (Note: LLM_MODEL is the default selected model, and it must be included in the AVAIL_LLM_MODELS switch list )
LLM_MODEL = "gpt-3.5-turbo" # optional ↓↓↓
AVAIL_LLM_MODELS = ["gpt-3.5-turbo", "api2d-gpt-3.5-turbo", "gpt-4", "api2d-gpt-4", "chatglm", "moss", "newbing", "newbing- free", "stack-claude"]
# P.S. Other available models include ["newbing-free", "jittorllms_rwkv", "jittorllms_pangualpha", "jittorllms_llama"]

# Execution of local LLM models such as ChatGLM CPU/GPU
LOCAL_MODEL_DEVICE = "cpu" # optional "cuda"

# Set the number of parallel threads of gradio (no need to modify)
CONCURRENT_COUNT = 100

# Add a live2d decoration
ADD_WAIFU = False

# Set the user name and password (no need to modify) (related functions are unstable, related to gradio version and network, if you use it locally, it is not recommended to add this)
# [("username", "password"), ("username2", "password2"), ...]
AUTHENTICATION = []

# Redirect the URL to achieve the function of replacing API_URL (under normal circumstances, do not modify it!!)
# (High-risk setting! By modifying this setting, you will completely expose your API-KEY and conversation privacy to the middleman you set!)
# Format {"https://api.openai.com/v1/chat/completions": "Fill in the redirected api.openai.com URL here"}
# For example API_URL_REDIRECT = {"https://api.openai.com/v1/chat/completions": "https://ai.open.com/api/conversation"}
API_URL_REDIRECT = {}

# If you need to run under the secondary path (under normal circumstances, do not modify!!) (you need to cooperate with modifying main.py to take effect!)
CUSTOM_PATH = "/"

# If you need to use newbing, put the long cookie of newbing here
NEWBING_STYLE = "creative" # ["creative", "balanced", "precise"]
# From now on, if you call the "newbing-free" model, you don't need to fill in NEWBING_COOKIES
NEWBING_COOKIES = """
your bing cookies here
"""

# If you need to use Slack Claude, see request_llm/README.md for the tutorial details
SLACK_CLAUDE_BOT_ID = ''
SLACK_CLAUDE_USER_TOKEN = ''
