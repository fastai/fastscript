from .fastscript import *

@call_parse
def main(
    msg:Param("The message", str),
    upper:Param("Convert to uppercase?", str2bool)=False,
):
    if upper: msg = msg.upper()
    print(msg)

