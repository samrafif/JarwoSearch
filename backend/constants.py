import inspect
import os

from yaml import load, dump
from dotenv import load_dotenv
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

YAML_FILE = "./config.yaml"
DEBUG = True

if DEBUG:
    load_dotenv()

class YamlConfig:
    def __init__(self) -> None:
        
        with open(YAML_FILE, "r") as f:
            self.config = load(f, Loader=Loader)
        
        self.load_configs()
        
    def load_configs(self):

        class_name = self.__class__.__name__.lower()
        base = self.config.get(class_name)
        if base is None: 
            raise ValueError(f"The base outer config of {class_name} does not exist")
        
        attributes = inspect.getmembers(self.__class__, lambda a:not(inspect.isroutine(a)))
        attributes = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]

        for k, v in attributes:
            value = base.get(k)
            if str(value).startswith("${") and str(value).endswith("}"):
                value = os.getenv(value[1:])

            if value is None: 
                raise ValueError(f"The variable of {k} does not exist in config")

            setattr(self, k, value)

class Database(YamlConfig):
    hostname: str = ""
    port: str= ""
    username: str = ""
    password: str = ""

a = Database()
print(a.password)