from toolbox import update_ui
from toolbox import CatchException, report_execption, write_results_to_file
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
fast_debug = False

def 生成函数注释(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, os
    print('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()

        i_say = f'Please provide an overview of the following program file and generate comments for all functions in the file. Use markdown table to output the results. The file name is {os.path.relpath(fp, project_folder)}, and the file content is ```{file_content}```'
        i_say_show_user = f'[{index}/{len(file_manifest)}] Please provide an overview of the following program file and generate comments for all functions: {os.path.abspath(fp)}'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the UI

        if not fast_debug: 
            msg = 'normal'
            # ** gpt request **
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                i_say, i_say_show_user, llm_kwargs, chatbot, history=[], sys_prompt=system_prompt)   # With timeout countdown

            chatbot[-1] = (i_say_show_user, gpt_say)
            history.append(i_say_show_user); history.append(gpt_say)
            yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the UI
            if not fast_debug: time.sleep(2)

    if not fast_debug: 
        res = write_results_to_file(history)
        chatbot.append(("Are you done?", res))
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # Refresh the UI



@CatchException
def 批量生成函数注释(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # Clear history to avoid overflow
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input'
        report_execption(chatbot, history, a=f"Parse project: {txt}", b=f"Cannot find local project or access denied: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the UI
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.py', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)]

    if len(file_manifest) == 0:
        report_execption(chatbot, history, a=f"Parse project: {txt}", b=f"No .tex files found: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the UI
        return
    yield from 生成函数注释(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
