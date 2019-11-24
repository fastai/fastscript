__all__ = ['Param', 'anno_parser', 'call_parse', 'bool_arg']

import inspect,sys,functools,sys,argparse

def bool_arg(v):
    if isinstance(v, bool): return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'): return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'): return False
    else: raise argparse.ArgumentTypeError('Boolean value expected.')

class Param:
    "A parameter in a function used in `anno_parser` or `call_parse`"
    def __init__(self, help=None, type=None, opt=True, action=None, nargs=None, const=None,
                 choices=None, required=None):
        self.help,self.type,self.opt,self.action,self.nargs = help,type,opt,action,nargs
        self.const,self.choices,self.required = const,choices,required

    @property
    def pre(self): return '--' if self.opt else ''
    @property
    def kwargs(self): return {k:v for k,v in self.__dict__.items() if v is not None and k!='opt'}

def anno_parser(func):
    "Look at params (annotated with `Param`) in func and return an `ArgumentParser`"
    p = argparse.ArgumentParser(description=func.__doc__)
    for k,v in inspect.signature(func).parameters.items():
        param = func.__annotations__.get(k, Param())
        if v.default == inspect.Parameter.empty: param.opt=False
        kwargs = param.kwargs
        if v.default != inspect.Parameter.empty: kwargs['default'] = v.default
        p.add_argument(f"{param.pre}{k}", **kwargs)
    return p

def call_parse(func):
    "Decorator to create a simple CLI from `func` using `anno_parser`"
    mod = inspect.getmodule(inspect.currentframe().f_back)
    if not mod: return func

    @functools.wraps(func)
    def _f(*args, **kwargs):
        args = anno_parser(func).parse_args()
        func(**args.__dict__)
    if mod.__name__=="__main__": return _f()
    else: return _f

