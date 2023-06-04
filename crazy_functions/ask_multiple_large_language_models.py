from toolbox import CatchException, update_ui
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import datetime
@CatchException
def 同时问询(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field, such as a paragraph to be translated or a path to a file to be processed
    llm_kwargs      Parameters for the GPT model, such as temperature and top_p, usually passed as-is
    plugin_kwargs   Parameters for the plugin model, such as temperature and top_p, usually passed as-is
    chatbot         Handle to the chat display box used for displaying to the user
    history         Chat history, previous context
    system_prompt   Silent prompt for the GPT model
    web_port        Port number on which the software is running
    """
    history = []  # Clear history to avoid overflow
    chatbot.append((txt, "Concurrently consulting ChatGPT and ChatGLM..."))
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the UI

    llm_kwargs['llm_model'] = 'chatglm&gpt-3.5-turbo'  # Support any number of llm interfaces separated by '&'
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=txt, inputs_show_user=txt, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
        sys_prompt=system_prompt,
        retry_times_at_unknown_error=0
    )

    history.append(txt)
    history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the UI


@CatchException
def 同时问询_指定模型(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             Text entered by the user in the input field, such as a paragraph to be translated or a path to a file to be processed
    llm_kwargs      Parameters for the GPT model, such as temperature and top_p, usually passed as-is
    plugin_kwargs   Parameters for the plugin model, such as temperature and top_p, usually passed as-is
    chatbot         Handle to the chat display box used for displaying to the user
    history         Chat history, previous context
    system_prompt   Silent prompt for the GPT model
    web_port        Port number on which the software is running
    """
    history = []  # Clear history to avoid overflow
    chatbot.append((txt, "Concurrently consulting ChatGPT and ChatGLM..."))
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the UI

    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    llm_kwargs['llm_model'] = plugin_kwargs.get("advanced_arg", 'chatglm&gpt-3.5-turbo')  # 'chatglm&gpt-3.5-turbo' # Support any number of llm interfaces separated by '&'
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=txt, inputs_show_user=txt, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
        sys_prompt=system_prompt,
        retry_times_at_unknown_error=0
    )

    history.append(txt)
    history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the UI
