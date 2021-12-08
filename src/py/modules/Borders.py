import imageio
import numpy as np

from src.sammie.py.modules.ModuleBase import ModuleBase
from src.sammie.py.util import imgutil
from src.sammie.py.util.imgutil import getPreviewImage


class BordersKeys:
    """Convenience class to access the keys as named entities rather than in an array"""
    inPreprocessedImg: str
    outBorderedImage: str

    def __init__(self, inputs, outputs):
        self.inPreprocessedImg = inputs[0]
        self.outBorderedImage = outputs[0]

class Borders(ModuleBase):

    keys: BordersKeys

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.log = 'Borders'
        self.trace('initialized')

    def unpackParams(self,borderwidth,**other):
        """unpack and possibly parse/cast all parameters coming from JS. The parameters from JS are defined in the params.tsx file of the respective step.
        The arrive as a dictionary on the py side and sometimes need some parsing. In any way this function provides a simple method to extract
        these parameters as named variables rather than using params['paramName1'] you can run it through this function."""
        #
        #respective
        return borderwidth[0]

    def run(self, action, params, inputkeys,outputkeys):
        self.keys = BordersKeys(inputkeys, outputkeys)

        #This is a stub and simply displays best practices on how to structure this function. Feel free to change it
        if action == 'apply':

            #Parse Parameters out of the dictionary arriving from JS
            borderwidth = self.unpackParams(**params)

            #get the input that this step is working on
            inputImg = np.copy(self.session.getData(self.keys.inPreprocessedImg))

            inputImg = imgutil.addBorder(inputImg,borderwidth,0)

            #Required: Notify the pipeline that the processed data is now available, so that the user can step to the next step
            #of the UI.
            self.onGeneratedData(self.keys.outBorderedImage, inputImg, params)

            #Generate an output that will go to javascript for displaying on the UI side
            return getPreviewImage(inputImg,self.keys.outBorderedImage)

    def exportData(self, key: str, path: str, **args):
        #Get the data that needs to be exported
        data = self.session.getData(key)

        # Write a file with this data or postprocess it in some way
        imageio.imsave(path, data)

