from .core import *

@call_parse
def main(msg:Param("The message", str),
         upper:Param("Convert to uppercase?", bool_arg)=False):
    msg = msg.upper() if upper else msg
    print(msg)
    return msg

