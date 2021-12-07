import numpy as np

from src.sammie.py.modules.ModuleBase import ModuleBase
from src.sammie.py.util.imgutil import getPreviewImage


class PreProcessingKeys:
    """Convenience class to access the keys as named entities rather than in an array"""
    inSomeInputKey: str
    outSomeOutputKey: str

    def __init__(self, inputs, outputs):
        self.inSomeInputKey = inputs[0]
        self.outSomeOutputKey = outputs[0]

class PreProcessing(ModuleBase):

    keys: PreProcessingKeys

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.log = 'PreProcessing'
        self.trace('initialized')

    def unpackParams(self,flip, thresholding, threshold ,**other):
        """unpack and possibly parse/cast all parameters coming from JS. The parameters from JS are defined in the params.tsx file of the respective step.
        The arrive as a dictionary on the py side and sometimes need some parsing. In any way this function provides a simple method to extract
        these parameters as named variables rather than using params['paramName1'] you can run it through this function."""
        #
        #respective
        return flip,thresholding, threshold

    def run(self, action, params, inputkeys,outputkeys):
        self.keys = PreProcessingKeys(inputkeys, outputkeys)

        #This is a stub and simply displays best practices on how to structure this function. Feel free to change it
        if action == 'apply':

            #Parse Parameters out of the dictionary arriving from JS
            flip, thresholding, threshold = self.unpackParams(**params)

            #get the input that this step is working on
            someInput:np.ndarray = np.copy(self.session.getData(self.keys.inSomeInputKey))

            #Flip Image
            if flip == 'hor': someInput = someInput[::-1,:]
            elif flip == 'ver': someInput = someInput[:,::-1]
            elif flip == 'center': someInput = someInput[::-1,::-1]

            #Threhshold the image
            if thresholding:
                someInput[someInput < threshold[0]] = 0
                someInput[someInput > threshold[1]] = 1

            #Required: Notify the pipeline that the processed data is now available, so that the user can step to the next step
            #of the UI.
            self.onGeneratedData(self.keys.outSomeOutputKey, someInput, params)

            #Generate an output that will go to javascript for displaying on the UI side
            preview = getPreviewImage(someInput,self.keys.outSomeOutputKey)

            return {'resultingImage':preview}

    def exportData(self, key: str, path: str, **args):
        #Get the data that needs to be exported
        data = self.session.getData(key)

        #Write a file with this data or postprocess it in some way
        #...

