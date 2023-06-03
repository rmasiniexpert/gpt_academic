import platform
from sys import stdout

if platform.system()=="Linux":
     pass
else:
     from colorama import init
     init()

# Do you like the elegance of Chinese characters?
def print red(*kw,**kargs):
     print("\033[0;31m",*kw,"\033[0m",**kargs)
def print green(*kw,**kargs):
     print("\033[0;32m",*kw,"\033[0m",**kargs)
def print huang(*kw,**kargs):
     print("\033[0;33m",*kw,"\033[0m",**kargs)
def print blue(*kw,**kargs):
     print("\033[0;34m",*kw,"\033[0m",**kargs)
def print purple(*kw,**kargs):
     print("\033[0;35m",*kw,"\033[0m",**kargs)
def print indigo(*kw,**kargs):
     print("\033[0;36m",*kw,"\033[0m",**kargs)

def print bright red(*kw,**kargs):
     print("\033[1;31m",*kw,"\033[0m",**kargs)
def print bright green(*kw,**kargs):
     print("\033[1;32m",*kw,"\033[0m",**kargs)
def print bright yellow(*kw,**kargs):
     print("\033[1;33m",*kw,"\033[0m",**kargs)
def print bright blue(*kw,**kargs):
     print("\033[1;34m",*kw,"\033[0m",**kargs)
def print bright purple(*kw,**kargs):
     print("\033[1;35m",*kw,"\033[0m",**kargs)
def print Bright Indigo(*kw,**kargs):
     print("\033[1;36m",*kw,"\033[0m",**kargs)

# Do you like the elegance of Chinese characters?
def sprint red(*kw):
     return "\033[0;31m"+' '.join(kw)+"\033[0m"
def sprintgreen(*kw):
     return "\033[0;32m"+' '.join(kw)+"\033[0m"
def sprint yellow(*kw):
     return "\033[0;33m"+' '.join(kw)+"\033[0m"
def sprint blue(*kw):
     return "\033[0;34m"+' '.join(kw)+"\033[0m"
def sprint purple(*kw):
     return "\033[0;35m"+' '.join(kw)+"\033[0m"
def sprint indigo(*kw):
     return "\033[0;36m"+' '.join(kw)+"\033[0m"
def sprint bright red (*kw):
     return "\033[1;31m"+' '.join(kw)+"\033[0m"
def sprint bright green (*kw):
     return "\033[1;32m"+' '.join(kw)+"\033[0m"
def sprint bright yellow (*kw):
     return "\033[1;33m"+' '.join(kw)+"\033[0m"
def sprint bright blue (*kw):
     return "\033[1;34m"+' '.join(kw)+"\033[0m"
def sprint bright purple (*kw):
     return "\033[1;35m"+' '.join(kw)+"\033[0m"
def sprint bright indigo (*kw):
     return "\033[1;36m"+' '.join(kw)+"\033[0m"
