import {EelResponse} from "../../../sammie/js/eel/eel";
import * as eel from "../../../sammie/js/eel/eel";
import * as self from "./params";
import {deletePipelineData, updatePipelineData} from "../../../sammie/js/state/stateutil";
import {PipelineImage} from "../../../sammie/js/types/datatypes";

export type PreProcessingResult = {
    resultingImage:PipelineImage
}
export async function runPreProcessing(curParams:self.Parameters, curStep:self.Step):Promise<EelResponse<PreProcessingResult>>{
    
    //Run the algorithm associated with this module
    var res:EelResponse<PreProcessingResult> = await eel.runStepAsync<PreProcessingResult>(self.moduleName,'apply',curParams,curStep)

    //update pipeline, on error, delete the output again.
    if(res.error) deletePipelineData(curStep.outputKeys.out);
    else updatePipelineData(curStep.outputKeys.out,res.data);

    return res
}