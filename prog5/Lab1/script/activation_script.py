import re
import sys
from urllib.request import urlopen
from requests import get
from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader



class URLLoader:
    def create_module(self, target):
        return None
    
    def exec_module(self, module):
        init_file_url = module.__spec__.origin + "/__init__.py"

        with urlopen(init_file_url) as page:
            source = page.read()
        code = compile(source, init_file_url, mode="exec")
        exec(code, module.__dict__)



class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available
        
    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}".format(self.url, name)
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin, is_package=True)
        
        else:
            return None
        
        
        
def url_hook(some_str):
      
    if not some_str.startswith(("http", "https")):
        raise ImportError
    
    try:
        with get(some_str) as page:
            data = page.text
        filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*/|[a-zA-Z_][a-zA-Z0-9_]*.py", data)
        modnames = {name[:-1] if name.endswith('/') else name[:-3] for name in filenames}
        return URLFinder(some_str, modnames)
    except:
        sys.exit(f"URL adress {some_str} error")



sys.path_hooks.append(url_hook)
print(sys.path_hooks)

sys.path.append("http://localhost:8000")

import myremotepackage                                                     # type: ignore
myremotepackage.myfoo()