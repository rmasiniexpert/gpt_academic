from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from toolbox import CatchException, report_execption, write_results_to_file
from toolbox import update_ui

def get_meta_information(url, chatbot, history):
     import requests
     import arxiv
     import difflib
     from bs4 import BeautifulSoup
     from toolbox import get_conf
     proxies, = get_conf('proxies')
     headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
     }
     # Send a GET request
     response = requests. get(url, proxies=proxies, headers=headers)

     # Parse the content of the web page
     soup = BeautifulSoup(response. text, "html. parser")

     def string_similar(s1, s2):
         return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

     profile = []
     # Get the title and author of all articles
     for result in soup. select(".gs_ri"):
         title = result.a.text.replace('\n', ' ').replace(' ', ' ')
         author = result.select_one(".gs_a").text
         try:
             citation = result.select_one(".gs_fl > a[href*='cites']").text # The number of citations is the text in the link, take it out directly
         except:
             citation = 'cited by 0'
         abstract = result.select_one(".gs_rs").text.strip() # Abstract the text in .gs_rs, need to clear the leading and trailing spaces
         search = arxiv. Search(
             query = title,
             max_results = 1,
             sort_by = arxiv.SortCriterion.Relevance,
         )
         try:
             paper = next(search.results())
             if string_similar(title, paper.title) > 0.90: # same paper
                 abstract = paper.summary.replace('\n', ' ')
                 is_paper_in_arxiv = True
             else: # different paper
                 abstract = abstract
                 is_paper_in_arxiv = False
             paper = next(search.results())
         except:
             abstract = abstract
             is_paper_in_arxiv = False
         print(title)
         print(author)
         print(citation)
         profile.append({
             'title': title,
             'author': author,
             'citation': citation,
             'abstract': abstract,
             'is_paper_in_arxiv': is_paper_in_arxiv,
         })

         chatbot[-1] = [chatbot[-1][0], title + f'\n\nIs it in arxiv (not in arxiv, you can't get a full abstract): {is_paper_in_arxiv}\n\n' + abstract]
         yield from update_ui(chatbot=chatbot, history=[]) # refresh interface
     return profile

@CatchException
def Google search assistant (txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
     # Basic information: features, contributors
     chatbot.append([
         "Function plugin function?",
         "Analyze all articles that appear on the Google Scholar search page provided by users: binary-husky, plugin initialization..."])
     yield from update_ui(chatbot=chatbot, history=history) # Refresh the interface

     # Try to import dependencies, if missing dependencies, give installation suggestions
     try:
         import arxiv
         import math
         from bs4 import BeautifulSoup
     except:
         report_execption(chatbot, history,
             a = f"Analysis item: {txt}",
             b = f"Failed to import software dependencies. Additional dependencies are required to use this module. The installation method is ```pip install --upgrade beautifulsoup4 arxiv```.")
         yield from update_ui(chatbot=chatbot, history=history) # Refresh the interface
         return

     # Clear history to avoid input overflow
     history = []
     meta_paper_info_list = yield from get_meta_information(txt, chatbot, history)
     batchsize = 5
     for batch in range(math.ceil(len(meta_paper_info_list)/batchsize)):
         if len(meta_paper_info_list[:batchsize]) > 0:
             i_say = "The following is the data of some academic literature, the following content is extracted:" + \
             "1. English title; 2. Chinese title translation; 3. Author; 4. Arxiv public (is_paper_in_arxiv); 4. Number of citations (cite); 5. Chinese abstract translation." + \
             f"The following is the information source: {str(meta_paper_info_list[:batchsize])}"

             inputs_show_user = f "Please analyze all articles appearing in this page: {txt}, this is batch {batch+1}"
             gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                 inputs=i_say, inputs_show_user=inputs_show_user,
                 llm_kwargs=llm_kwargs, chatbot=chatbot, history=[],
                 sys_prompt="You are an academic translator, please extract information from the data. You must use Markdown tables. You must process document by document."
             )

             history.extend([ f "{batch+1} batch", gpt_say ])
             meta_paper_info_list = meta_paper_info_list[batchsize:]

     chatbot.append(["Status?",
         "It's all done, you can try to let AI write a Related Works, for example, you can continue to enter Write a \"Related Works\" section about \"the research field you searched\" for me."])
     msg = 'normal'
     yield from update_ui(chatbot=chatbot, history=history, msg=msg) # refresh interface
     res = write_results_to_file(history)
     chatbot.append(("Are you done?", res));
     yield from update_ui(chatbot=chatbot, history=history, msg=msg) # refresh interface
