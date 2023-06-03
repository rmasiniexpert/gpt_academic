def get_current_version():
     import json
     try:
         with open('./version', 'r', encoding='utf8') as f:
             current_version = json. loads(f. read())['version']
     except:
         current_version = ""
     return current_version


def auto_update(raise_error=False):
     """
     One-click update agreement: query version and user opinions
     """
     try:
         from toolbox import get_conf
         import requests
         import time
         import json
         proxies, = get_conf('proxies')
         response = requests. get(
             "https://raw.githubusercontent.com/binary-husky/chatgpt_academic/master/version", proxies=proxies, timeout=5)
         remote_json_data = json. loads(response. text)
         remote_version = remote_json_data['version']
         if remote_json_data["show_feature"]:
             new_feature = "New feature:" + remote_json_data["new_feature"]
         else:
             new_feature = ""
         with open('./version', 'r', encoding='utf8') as f:
             current_version = f. read()
             current_version = json. loads(current_version)['version']
         if (remote_version - current_version) >= 0.01:
             from colorful import print bright yellow
             print bright yellow (
                 f'\nA new version is available. New version: {remote_version}, current version: {current_version}. {new_feature}')
             print('(1) Github update address:\nhttps://github.com/binary-husky/chatgpt_academic\n')
             user_instruction = input('(2) Is it possible to update the code with one click (Y+Enter=confirm, input other/no input+Enter=no update)?')
             if user_instruction in ['Y', 'y']:
                 path = backup_and_download(current_version, remote_version)
                 try:
                     patch_and_restart(path)
                 except:
                     msg = 'Update failed. '
                     if raise_error:
                         from toolbox import trimmed_format_exc
                         msg += trimmed_format_exc()
                     print(msg)
             else:
                 print('Automatic Updater: Disabled')
                 return
         else:
             return
     except:
         msg = 'Auto Updater: Disabled'
         if raise_error:
             from toolbox import trimmed_format_exc
             msg += trimmed_format_exc()
         print(msg)

def warm_up_modules():
     print('Warming up some modules...')
     from request_llm.bridge_all import model_info
     enc = model_info["gpt-3.5-turbo"]['tokenizer']
     enc.encode("Module preheating", disallowed_special=())
     enc = model_info["gpt-4"]['tokenizer']
     enc.encode("Module preheating", disallowed_special=())

if __name__ == '__main__':
     import os
     os.environ['no_proxy'] = '*' # avoid accidental pollution of proxy network
     from toolbox import get_conf
     proxies, = get_conf('proxies')
     check_proxy(proxies)
