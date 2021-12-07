import {Pipeline} from "../../sammie/js/types/pipelinetypes";
import initDemoPipeline from './DemoPipeline'

/**Main Function to initialize pipelines*/
export function getPipelineDefinitions() {
    //You need to initiate pipeline defintions here and add them to the returned array.
    const d = initDemoPipeline();
    return [d];
}
