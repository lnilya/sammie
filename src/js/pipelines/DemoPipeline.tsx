import React from "react";
import * as util from '../../sammie/js/pipelines/pipelineutil'
import {suggestSuffixedFileName} from '../../sammie/js/pipelines/pipelineutil'
import {Pipeline} from "../../sammie/js/types/pipelinetypes";
import ResponsiveEmbed from 'react-responsive-embed'
import * as PreProcessingParams from '../modules/PreProcessing/params'
import PreProcessing from "../modules/PreProcessing/PreProcessing";
//%NEWMODULE_IMPORT%

const inputKeys = {
    rawImage: 'Raw Image',
}
const dataKeys = {
    processedImage: 'Processed Image', //example, some step for example adds these two images into one.
}

const helpScreen = <div>
    Here is the main Help Component for this Pipeline. You can even add a Video like so:
    <ResponsiveEmbed src='https://www.youtube.com/embed/QtzI1SwOdbY' allowFullScreen />
</div>

function getPipeline(): Pipeline {
    
    const datasetDesc = 'This description appears in the file loader when loading this file.'
    
    return {
        steps: [
            //No Steps defined yet. Use the main create Script to add Steps automatically.
            //This will work, as long as you keep the comment below.
            { 
            title:'PreProcessing',
            moduleID:'PreProcessing',
            renderer: <PreProcessing/>,
            parameters:PreProcessingParams.parameters,
            inputKeys:{in:inputKeys.rawImage},
            outputKeys:{out:dataKeys.processedImage}
        } as PreProcessingParams.Step,
        //%NEWMODULE_STEP%
        ],
        
        disableBatchMode:true, //wether or not batch mode is allowed.
        
        name: 'Demo', //name of your pipeline
        
        //Define what data needs to be provided in DataInput screen to start the pipeline
        inputs: [
            {
                key: inputKeys.rawImage,
                title: 'Grayscale Image', description: datasetDesc,
                loaders: {'jpg,png,tif': 'loadIntensityImage'}, //this loader does not exist and is just for Demo purposes
                postProcessForJS: util.postProcessForImage //postprocessing
            }
        ],
        //Define what the outputs of this Pipeline are
        outputs: [
            {
                requiredInput: dataKeys.processedImage,
                title:'Sum of Two images',
                description:'This is the description that appears in the Export file screen.',
                
                //Should define a suggestion function for naming the output, makes it a lot easier for user to store files.
                suggestDestinationOutput:{
                    pipelineInputKey:inputKeys.rawImage,
                    transform:suggestSuffixedFileName('_sum','png')
                },
            }
        ],
        
        //Info for user
        descriptions:{
            title:'Demo Pipeline',
            description:'This description appears in switch pipeline screen.',
            helpscreen:helpScreen
        }
    }
}

export default getPipeline;