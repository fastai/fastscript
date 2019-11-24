from .fastscript import *

@call_parse
def main(msg:Param("The message", str),
         upper:Param("Convert to uppercase?", bool_arg)=False):
    print(msg.upper() if upper else msg)

