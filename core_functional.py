# 'primary' color corresponds to primary_hue in theme.py
# 'secondary' color corresponds to neutral_hue in theme.py
# 'stop' color corresponds to color_er in theme.py
# The default button color is secondary
from toolbox import clear_line_break


def get_core_functions():
     return {
         "English Academic Polish": {
             # Preface
             "Prefix": r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                         r"improve the spelling, grammar, clarity, decision and overall readability. When necessary, rewrite the whole sentence." +
                         r"Furthermore, list all modification and explain the reasons to do so in markdown table." + "\n\n",
             # Postscript
             "Suffix": r"",
             "Color": r"secondary", # button color
         },
         "Chinese Academic Polish": {
             "Prefix": r"As a Chinese academic paper writing improvement assistant, your task is to improve the spelling, grammar, clarity, conciseness and overall readability of the text provided," +
                         r"Also break up long sentences, reduce repetition, and suggest improvements. Please only provide corrected versions of the text, avoid including explanations. Please edit the text below" + "\n\n",
             "Suffix": r"",
         },
         "Find syntax errors": {
             "Prefix": r"Can you help me ensure that the grammar and the spelling is correct?" +
                         r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good." +
                         r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, " +
                         r"put the original text the first column, " +
                         r"put the corrected text in the second column and highlight the key words you fixed.""\n"
                         r"Example:""\n"
                         r"Paragraph: How is you? Do you know what is it?""\n"
                         r"| Original sentence | Corrected sentence |""\n"
                         r"| :--- | :--- |""\n"
                         r"| How **is** you? | How **are** you? |""\n"
                         r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n"
                         r"Below is a paragraph from an academic paper."
                         r"You need to report all grammar and spelling mistakes as the example before."
                         + "\n\n",
             "Suffix": r"",
             "PreProcess": clear_line_break, # preprocessing: clear line break
         },
         "Chinese to English": {
             "Prefix": r"Please translate following sentence to English:" + "\n\n",
             "Suffix": r"",
         },
         "Academic Chinese-English translation": {
             "Prefix": r"I want you to act as a scientific English-Chinese translator, " +
                         r"I will provide you with some paragraphs in one language " +
                         r"and your task is to accurately and academically translate the paragraphs only into the other language." +
                         r"Do not repeat the original provided paragraphs after translation." +
                         r"You should use artificial intelligence tools, " +
                         r"such as natural language processing, and rhetorical knowledge " +
                         r"and experience about effective writing techniques to reply. " +
                         r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:" + "\n\n",
             "Suffix": "",
             "Color": "secondary",
         },
         "English to Chinese": {
             "Prefix": r" translates into authentic Chinese: " + "\n\n",
             "Suffix": r"",
         },
         "find pictures": {
             "Prefix": r"I need you to find a picture on the Internet. Use the Unsplash API (https://source.unsplash.com/960x640/?<English keywords>) to get the picture URL," +
                         r"Then please use Markdown format packaging, and do not have backslashes, do not use code blocks. Now, please send me pictures as described below: " + "\n\n",
             "Suffix": r"",
         },
         "interpret code": {
             "Prefix": r"Please explain the following code:" + "\n```\n",
             "Suffix": "\n```\n",
         },
         "Reference to Bib": {
             "Prefix": r"Here are some bibliography items, please transform them into bibtex style." +
                         r"Note that, reference styles maybe more than one kind, you should transform each item correctly." +
                         r"Items need to be transformed:",
             "Suffix": r"",
             "Visible": False,
         }
     }
