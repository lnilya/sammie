import os.path
import pickle
import time
from typing import Dict

from src.sammie.py.SessionData import SessionData
from src.sammie.py.modules.ModuleBase import ModuleBase


def __getBaseAggregateFile():
    return {'data':{},'created':time.time()}

def __getDataSetInfoObject(curData):
    if len(curData['data']) == 0:
        return {'exists':True, 'info':'File exists, but contains no results yet.', 'ready':True}

    return {'exists':True, 'info':'File contains results from %d batches'%(len(curData['data'])), 'ready':True}

def __getBatchData(session:SessionData, modulesById:Dict[str, ModuleBase],scalePxToNm:float = None):

    return {'images':[], 'scale':1}

def appendToDemoCSV_Info(destinationPath:str):
    filename = os.path.basename(destinationPath)
    ext = filename.split('.')
    if len(ext) > 1:
        ext = ext[-1]
    else:
        return {'exists':False, 'info': 'Add a file with a *.cells extension.', 'ready': False}

    if ext != 'cells':
        return {'exists':False, 'info': 'File extension should be *.cells', 'ready': False}

    if not os.path.exists(destinationPath):
        return {'exists':False, 'ready':True,'info':'The selected file will be created on first export.'}

    try:
        with open(destinationPath, 'rb') as handle:
            curData = pickle.load(handle)
    except:
        return {'exists':True, 'info':'File exists but is corrupt and can\'t be loaded. It will be overwritten on export.', 'ready':True}

    return __getDataSetInfoObject(curData)

def appendToDemoCSV_Reset(destinationPath:str):
    with open(destinationPath, 'wb') as handle:
        pickle.dump(__getBaseAggregateFile(), handle, protocol=pickle.HIGHEST_PROTOCOL)

    return True

def appendToDemoCSV(destinationPath:str,data:SessionData, modulesById:Dict[str, ModuleBase], batchNum:int, adtlParams:Dict = None):
    scale = None
    if '1px' in adtlParams: scale = adtlParams['1px']

    curData:Dict = __getBaseAggregateFile()

    reset:bool = False
    #Read file if it exists
    if os.path.exists(destinationPath):
        try:
            with open(destinationPath, 'rb') as handle:
                curData = pickle.load(handle)
        except:
            #reset file
            reset = True
            curData = __getBaseAggregateFile(scale)
            appendToDemoCSV_Reset(destinationPath)

    overwritten:bool = batchNum in curData['data']

    #Add the data from this batch
    curData['data'][batchNum] = __getBatchData(data,modulesById, scale)

    #Overwrite with new data
    with open(destinationPath, 'wb') as handle:
        pickle.dump(curData, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if overwritten and not reset:
        msg = 'Overwritten batch %d results in dataset: Currently %d entries. '%(batchNum, len(curData['data']))
    elif not overwritten and not reset:
        msg = 'Added batch %d results to dataset. Currently %d entries. '%(batchNum, len(curData['data']))
    else:
        msg = 'Reset file and added batch %d results to dataset.'%(batchNum)

    return {'msg':msg,'info':__getDataSetInfoObject(curData)}
