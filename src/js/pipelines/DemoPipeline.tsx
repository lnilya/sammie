import React from "react";
import * as util from '../../sammie/js/pipelines/pipelineutil'
import {suggestSuffixedFileName} from '../../sammie/js/pipelines/pipelineutil'
import {Pipeline} from "../../sammie/js/types/pipelinetypes";
import ResponsiveEmbed from 'react-responsive-embed'
import * as PreProcessingParams from '../modules/PreProcessing/params'
import PreProcessing from "../modules/PreProcessing/PreProcessing";
import * as BordersParams from '../modules/Borders/params'
import Borders from "../modules/Borders/Borders";
//%NEWMODULE_IMPORT%

const inputKeys = {
    rawImage: 'Raw Image',
}
const dataKeys = {
    processedImage: 'Processed Image', //example, some step for example adds these two images into one.
    borderedImage: 'Bordered Image', //example, some step for example adds these two images into one.
}

const helpScreen = <div>
    Here is the main Help Component for this Pipeline. You can even add a Video like so:
    <ResponsiveEmbed src='https://www.youtube.com/embed/QtzI1SwOdbY' allowFullScreen/>
</div>

function getPipeline(): Pipeline {
    
    const datasetDesc = 'This description appears in the file loader when loading this file.'
    
    return {
        steps: [
            //No Steps defined yet. Use the main create Script to add Steps automatically.
            //This will work, as long as you keep the comment below.
            {
                title: 'PreProcessing',
                moduleID: 'PreProcessing',
                renderer: <PreProcessing/>,
                parameters: PreProcessingParams.parameters,
                inputKeys: {in: inputKeys.rawImage},
                outputKeys: {out: dataKeys.processedImage}
            } as PreProcessingParams.Step,
            {
                title: 'Borders',
                moduleID: 'Borders',
                renderer: <Borders/>,
                parameters: BordersParams.parameters,
                inputKeys: {in:dataKeys.processedImage},
                outputKeys: {out:dataKeys.borderedImage}
            } as BordersParams.Step,
            //%NEWMODULE_STEP%
        ],
        
        disableBatchMode: true, //wether or not batch mode is allowed.
        
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
                title: 'Result of Step 1',
                description: 'This is the description that appears in the Export file screen.',
                
                //Should define a suggestion function for naming the output, makes it a lot easier for user to store files.
                suggestDestinationOutput: {
                    pipelineInputKey: inputKeys.rawImage,
                    transform: suggestSuffixedFileName('_processed', 'jpg')
                },
            },
            {
                requiredInput: dataKeys.borderedImage,
                title: 'Result of Step 2',
                description: 'This is the description that appears in the Export file screen.',
                
                //Should define a suggestion function for naming the output, makes it a lot easier for user to store files.
                suggestDestinationOutput: {
                    pipelineInputKey: inputKeys.rawImage,
                    transform: suggestSuffixedFileName('_bordered', 'png')
                },
            }
        ],
        aggregatorOutputs: [
            {
                aggregatorID: 'appendToDemoCSV',
                title: 'CSV Output',
                description: 'For Demo purposes appends some data from the processed images into a CSV file',
                requiredInputs: [dataKeys.processedImage]
            }
        ],
        
        //Info for user
        descriptions: {
            title: 'Demo Pipeline',
            description: 'This description appears in switch pipeline screen.',
            helpscreen: helpScreen
        }
    }
}

export default getPipeline;