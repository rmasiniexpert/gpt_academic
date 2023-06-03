from toolbox import HotReload # HotReload means hot update. After modifying the function plug-in, there is no need to restart the program, and the code will take effect directly


def get_crazy_functions():
     ####################### First set of plugins ########################## ###
     from crazy_functions. read article write summary import read article write summary
     from crazy_functions. Generate function comments import Generate function comments in batches
     from crazy_functions. parse project source code import parse project itself
     from crazy_functions. Parse project source code import Parse a Python project
     from crazy_functions. Parse the project source code import Parse the header file of a C project
     from crazy_functions. parse project source code import parse a C project
     from crazy_functions. Parsing project source code import Parsing a Golang project
     from crazy_functions. Parse project source code import Parse a Rust project
     from crazy_functions. Parsing project source code import Parsing a Java project
     from crazy_functions. Parse project source code import Parse a front-end project
     from crazy_functions. Advanced function function template import Advanced function template function
     from crazy_functions. The code is rewritten as full English_Multi-threaded import All projects switch to English
     from crazy_functions.Latex full text polish import Latex English polish
     from crazy_functions. Ask multiple large language models import and ask at the same time
     from crazy_functions. Parsing project source code import Parsing a Lua project
     from crazy_functions. Parsing project source code import Parsing a CSharp project
     from crazy_functions.summarize word document import summarize word document
     from crazy_functions. parse JupyterNotebook import parse ipynb file
     from crazy_functions.conversation-history import dialog-history-archive
     from crazy_functions.conversation history import load conversation history
     from crazy_functions.conversation-history import delete all local conversation history
    
from crazy_functions. Batch Markdown translation import Markdown English to Chinese
     function_plugins = {
         "Parse the entire Python project": {
             "Color": "stop", # button color
             "Function": HotReload (parse a Python project)
         },
         "Load conversation history archive (upload archive first or enter path)": {
             "Color": "stop",
             "AsButton": False,
             "Function": HotReload (load conversation history archive)
         },
         "Delete all local conversation history (please proceed with caution)": {
             "AsButton": False,
             "Function": HotReload (delete all local conversation history)
         },
         "[Test function] Parse Jupyter Notebook files": {
             "Color": "stop",
             "AsButton": False,
             "Function": HotReload (parse ipynb file),
             "AdvancedArgs": True, # When calling, invoke the advanced parameter input area (default False)
             "ArgsReminder": "If 0 is entered, the Markdown block in the notebook will not be parsed", # Display hints in the advanced parameter input area
         },
         "Batch summary Word document": {
             "Color": "stop",
             "Function": HotReload (summarize word document)
         },
         "Parse the entire C++ project header file": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse a header file of a C project)
         },
         "Parse the entire C++ project (.cpp/.hpp/.c/.h)": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse a C project)
         },
         "Parse the entire Go project": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse a Golang project)
         },
         "Parse the entire Rust project": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse a Rust project)
         },
         "Parse the entire Java project": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse a Java project)
         },
         "Parse the entire front-end project (js, ts, css, etc.)": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse a front-end project)
         },
         "Parse the entire Lua project": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse a Lua project)
         },
         "Parse the entire CSharp project": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse a CSharp project)
},
         "Read Tex paper and write abstract": {
             "Color": "stop", # button color
             "Function": HotReload (read article and write summary)
         },
         "Markdown/Readme English translation": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Color": "stop",
             "Function": HotReload (Markdown English translation)
         },
         "Batch Generate Function Comments": {
             "Color": "stop", # button color
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (generate function comments in batches)
         },
         "Save current conversation": {
             "Function": HotReload (conversation history archive)
         },
         "[Multi-threaded Demo] parse this project itself (source code self-decoding)": {
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (parse the project itself)
         },
         "[Old Demo] Switch the source code of this project to full English": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (All items switch to English)
         },
         "[Plugin demo] Today in history": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Function": HotReload (higher-order function template function)
         },

     }
     ####################### Second set of plugins ########################## ###
     # [Second set of plugins]: fully tested
from crazy_functions. Batch summary PDF documents import Batch summary PDF documents
     # from crazy_functions. Batch summary of PDF documents pdfminer import Batch summary of PDF documents pdfminer
     from crazy_functions.Batch translation of PDF documents_Multi-threaded import Batch translation of PDF documents
     from crazy_functions. Google Search Assistant import Google Search Assistant
     from crazy_functions. Understand PDF document content import Understand PDF document content standard file input
     from crazy_functions.Latex full text polish import Latex Chinese polish
     from crazy_functions.Latex full text polishing import Latex English error correction
     from crazy_functions.Latex full text translation import Latex Chinese to English
     from crazy_functions.Latex full text translation import Latex English to Chinese
     from crazy_functions. Batch Markdown translation import Markdown Chinese to English

     function_plugins. update({
         "Batch translation of PDF documents (multi-threaded)": {
             "Color": "stop",
             "AsButton": True, # add to the dropdown menu
             "Function": HotReload (batch translation of PDF documents)
         },
         "Ask for multiple GPT models": {
             "Color": "stop", # button color
             "Function": HotReload (ask simultaneously)
         },
         "[Test function] Batch summarize PDF documents": {
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Function": HotReload (batch summarize PDF documents)
         },
         # "[Test function] Batch summary PDF documents pdfminer": {
         # "Color": "stop",
         # "AsButton": False, # Add to the drop-down menu
         # "Function": HotReload (batch summary of PDF documents pdfminer)
         # },
         "Google Scholar (enter the url of the Google Scholar page)": {
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (Google search assistant)
         },
         "Understand PDF document content (imitate ChatPDF)": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (understand PDF document content standard file input)
         },
         "Full-text editing of English Latex project (enter path or upload compressed package)": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (Latex English polish)
         },
         "English Latex project full-text error correction (enter path or upload compressed package)": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (Latex English error correction)
         },
         "Full-text editing of Chinese Latex project (enter path or upload compressed package)": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (Latex Chinese polish)
         },
         "Chinese-English translation of the full text of the Latex project (enter the path or upload the compressed package)": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (Latex Chinese to English)
         },
         "English to Chinese translation of the full text of the Latex project (enter the path or upload the compressed file)": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (Latex English translation)
         },
"Batch Markdown Chinese-English translation (enter path or upload compressed file)": {
             # HotReload means hot update. After modifying the function plug-in code, there is no need to restart the program, and the code will take effect directly
             "Color": "stop",
             "AsButton": False, # add to dropdown menu
             "Function": HotReload (Markdown Chinese to English)
         },


     })

     ####################### Third set of plugins ########################## ###
     # [Third group of plugins]: Function plugins that have not been fully tested

     try:
         from crazy_functions. Download arxiv paper translation abstract import Download arxiv paper and translate abstract
         function_plugins. update({
             "One-click download of arxiv papers and translate the abstract (first enter the number in the input, such as 1812.10695)": {
                 "Color": "stop",
                 "AsButton": False, # add to dropdown menu
                 "Function": HotReload (download arxiv paper and translate abstract)
             }
         })
     except:
         print('Load function plugin failed')

     try:
         from crazy_functions. Networked ChatGPT import Connect to the network to answer questions
         function_plugins. update({
             "Connect to the network to answer the question (enter the question first, then click the button, you need to access Google)": {
                 "Color": "stop",
                 "AsButton": False, # add to dropdown menu
                 "Function": HotReload (connect to the network to answer questions)
             }
         })
     except:
         print('Load function plugin failed')

     try:
         from crazy_functions. Parse project source code import Parse any code project
         function_plugins. update({
             "Parse project source code (manually specify and filter source code file types)": {
                 "Color": "stop",
                 "AsButton": False,
                 "AdvancedArgs": True, # When calling, invoke the advanced parameter input area (default False)
                 "ArgsReminder": "Separate with commas when inputting, * means wildcard, add ^ means no match; no input means all matches. For example: \"*.c, ^*.cpp, config.toml, ^*.toml \"", # The display prompt of the advanced parameter input area
                 "Function": HotReload (parse any code item)
             },
         })
     except:
         print('Load function plugin failed')

     try:
         from crazy_functions. Query multiple large language models import while querying_specified model
         function_plugins. update({
             "Ask multiple GPT models (manually specify which models to ask)": {
                 "Color": "stop",
                 "AsButton": False,
                 "AdvancedArgs": True, # When calling, invoke the advanced parameter input area (default False)
                 "ArgsReminder": "Support any number of llm interfaces, separated by & symbols. For example, chatglm&gpt-3.5-turbo&api2d-gpt-4", # The display prompt of the advanced parameter input area
                 "Function": HotReload (simultaneously query_specified model)
             },
         })
     except:
         print('Load function plugin failed')

     try:
         from crazy_functions.image generation import image generation
         function_plugins. update({
             "Image generation (switch the model to openai or api2d first)": {
                 "Color": "stop",
                 "AsButton": False,
                 "AdvancedArgs": True, # When calling, invoke the advanced parameter input area (default False)
                 "ArgsReminder": "Enter the resolution here, such as 256x256 (default)", # The display prompt of the advanced parameter input area
                 "Function": HotReload (image generation)
             },
         })
     except:
         print('Load function plugin failed')
            
try:
         from crazy_functions. Summarize audio and video import Summarize audio and video
         function_plugins. update({
             "Batch summary of audio and video (input path or upload compressed package)": {
                 "Color": "stop",
                 "AsButton": False,
                 "Advanced Args": True,
                 "ArgsReminder": "Call the openai api to use the whisper-1 model, currently supported formats: mp4, m4a, wav, mpga, mpeg, mp3. Here you can enter parsing tips, for example: parsing for Simplified Chinese (default).",
                 "Function": HotReload (summary audio and video)
             }
         })
     except:
         print('Load function plugin failed')

     try:
         from crazy_functions. Mathematics animation generation manim import animation generation
         function_plugins. update({
             "Mathematical animation generation (Manim)": {
                 "Color": "stop",
                 "AsButton": False,
                 "Function": HotReload (animation generation)
             }
         })
     except:
         print('Load function plugin failed')

     try:
         from crazy_functions. Batch Markdown translation import Markdown translation specified language
         function_plugins. update({
             "Markdown translation (manually specify language)": {
                 "Color": "stop",
                 "AsButton": False,
                 "Advanced Args": True,
                 "ArgsReminder": "Please enter the language you want to translate into, the default is Chinese.",
                 "Function": HotReload (Markdown translation specified language)
             }
         })
     except:
         print('Load function plugin failed')

     try:
         from crazy_functions.Langchain Knowledge Base import Knowledge Base Q&A
         function_plugins. update({
             "[The function is not yet stable] Build the knowledge base (please upload the file material first)": {
                 "Color": "stop",
                 "AsButton": False,
                 "Advanced Args": True,
                 "ArgsReminder": "The knowledge base name id to be injected, the default is default",
                 "Function": HotReload (Knowledge Base Questions and Answers)
             }
         })
     except:
         print('Load function plugin failed')

     try:
         from crazy_functions.Langchain knowledge base import Read knowledge base to answer
         function_plugins. update({
             "[Feature is not yet stable] Knowledge Base Q&A": {
                 "Color": "stop",
                 "AsButton": False,
                 "Advanced Args": True,
                 "ArgsReminder": "The name id of the knowledge base to be extracted, the default is default, you need to call to build the knowledge base first",
                 "Function": HotReload (read the knowledge base to answer)
             }
         })
     except:
         print('Load function plugin failed')

     ####################### nth group of plugins ########################## ###
     return function_plugins
