import {EelResponse} from "../../../sammie/js/eel/eel";
import * as eel from "../../../sammie/js/eel/eel";
import * as self from "./params";
import {deletePipelineData, updatePipelineData} from "../../../sammie/js/state/stateutil";
import {PipelineImage} from "../../../sammie/js/types/datatypes";

export async function runBorders(curParams:self.Parameters, curStep:self.Step):Promise<EelResponse<PipelineImage>>{
    
    //Run the algorithm associated with this module in python
    var res:EelResponse<PipelineImage> = await eel.runStepAsync<PipelineImage>(self.moduleName,'apply',curParams,curStep)

    //update pipeline, on error, delete the output again.
    if(res.error) deletePipelineData(curStep.outputKeys.out);
    else updatePipelineData(curStep.outputKeys.out,res.data);

    return res
}