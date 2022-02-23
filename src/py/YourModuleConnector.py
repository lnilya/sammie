from typing import Dict
from src.py import loaders
from src.py import aggregators

from src.sammie.py.ModuleConnector import ModuleConnector, AggregatorReturn, AggregatorFileInfo, LoaderResult
from src.sammie.py.SessionData import SessionData
from src.sammie.py.modules.ModuleBase import ModuleBase


class YourModuleConnector(ModuleConnector):
    def runLoader(self, loaderName: str, asPreview: bool, key: str, filePath: str, loaderArgs:Dict) -> LoaderResult:
        loaderFun = getattr(loaders, loaderName)  # will throw an error if doesnt exist
        return loaderFun(asPreview, key, filePath, **loaderArgs)

    def resetAggregatorFile(self, aggregatorID: str, destinationPath: str) -> bool:
        aggregatorFun = getattr(aggregators, aggregatorID + '_Reset')
        return aggregatorFun(destinationPath)

    def getAggregatorFileInfo(self, aggregatorID: str, destinationPath: str) -> AggregatorFileInfo:
        aggregatorFun = getattr(aggregators, aggregatorID + '_Info')
        return aggregatorFun(destinationPath)

    def runAggregator(self, aggregatorID: str, destinationPath: str, data: SessionData,
                      modulesById: Dict[str, ModuleBase], batchNum: int, adtlParams: Dict = None) -> AggregatorReturn:
        aggregatorFun = getattr(aggregators, aggregatorID)
        return aggregatorFun(destinationPath, data, modulesById, batchNum, adtlParams)

    def initializeModule(self, moduleID: str, moduleName: str, params: Dict, session: SessionData) -> ModuleBase:
        if moduleName == 'PreProcessing':
            from src.py.modules.PreProcessing import PreProcessing
            return PreProcessing(moduleID,session)
        elif moduleName == 'Borders':
            from src.py.modules.Borders import Borders
            return Borders(moduleID,session)
        # %NEW_MODULE%
        # Keep the New Module Comment at this location, for automatically adding new modules via scripts. Do not delete it, or the script will not work.