from src.py.YourModuleConnector import YourModuleConnector
from src.sammie.py.ModuleConnector import ModuleConnector


#Main file linking the Algorithm to the SAMMIE Framework

#Instance of a module connector. See ModuleConnector class in Sammie framework for the interface it needs to have.
def getModuleConnector()->ModuleConnector:
    return YourModuleConnector()