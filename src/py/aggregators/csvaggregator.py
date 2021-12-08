import csv
import os.path
from typing import Dict, List

import numpy as np

from src.sammie.py.ModuleConnector import AggregatorReturn, AggregatorFileInfo
from src.sammie.py.SessionData import SessionData
from src.sammie.py.modules.ModuleBase import ModuleBase


def __getTitleRow():
    """CSV Title ROW"""
    return ['Batch', 'Image Width', 'Image Height', 'Avg. Brightness']


def __getInfo(curData:List) -> AggregatorFileInfo:
    if len(curData) <= 1:
        return AggregatorFileInfo(True,True, 'File exists, but contains no results yet.')

    return AggregatorFileInfo(True,True, 'File contains results from %d batches'%(len(curData)-1))


def appendToDemoCSV_Info(destinationPath:str)->AggregatorFileInfo:
    """Generates some info on the file, wether it exists, has the right extensions etc.
    This is purely for UI purposes and can be skipped."""

    #Check if our extension is CSV
    if destinationPath[-3:] != 'csv':
        return AggregatorFileInfo(False, False, 'File should have a *.csv extension.')

    #Does the file exist?
    if not os.path.exists(destinationPath):
        return AggregatorFileInfo(False,True,'The selected file will be created on first export.')

    #If it exists get some information from the file
    try:
        with open(destinationPath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            rows = [r for r in reader]
    except:
        #if it cannot be read for some other reason.
        return AggregatorFileInfo(True,True,'File exists but is corrupt and can\'t be loaded. It will be overwritten on export.')

    return __getInfo(rows)

def appendToDemoCSV_Reset(destinationPath:str)->bool:
    """Reset function, writes a blank CSV file to the given location"""

    #Just writes the header into the CSV
    with open(destinationPath, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write header
        wr.writerow(__getTitleRow())

    return True

def appendToDemoCSV(destinationPath:str,data:SessionData, modulesById:Dict[str, ModuleBase], batchNum:int, adtlParams:Dict = None)->AggregatorReturn:
    """Main Aggregator function that writes some information about the processed image into a growing CSV file"""

    #Open the file and read current data
    created = False
    try:
        with open(destinationPath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            rows = [r for r in reader]
        #check if row exists and store its index
        rnum = [i for i,r in enumerate(rows) if r[0] == str(batchNum)]
    except:
        created = True
        rnum = []
        rows = [__getTitleRow()]


    #Get data to write into CSV - very simple here. But we can communicate via modulesById Parameter with any intiated module
    #in the current pipeline and ask it to provide information/generate data.
    img = data.getData('Processed Image')
    newRow = [batchNum, img.shape[1], img.shape[0], np.mean(img)]
    overwritten = False

    if len(rnum) > 0:#row exists we need to replace it
        rows[int(rnum[0])] = newRow
        overwritten = True
    else: #append the new batch
        rows += [newRow]

    #overwrite existing file with new data
    with open(destinationPath, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # write rows, which include header
        for r in rows: wr.writerow(r)



    #Generate some information for the user (will be displayed in a toast in the export aggregate screen).
    if overwritten and not created:
        msg = 'Overwritten batch %d results in dataset: Currently %d entries. '%(batchNum, len(rows)-1)
    elif not created:
        msg = 'Added batch %d results to dataset. Currently %d entries. '%(batchNum, len(rows) - 1)
    else:
        msg = 'Created file and added results from batch %d.'%(batchNum)

    ret = AggregatorReturn(msg, __getInfo(rows))