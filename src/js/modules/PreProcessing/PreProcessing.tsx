import React from "react";
import {atomFamily, useRecoilState, useRecoilValue} from "recoil";
import * as alg from "../../../sammie/js/state/algstate";
import * as ui from "../../../sammie/js/state/uistates";
import * as eventbus from "../../../sammie/js/state/eventbus";
import * as self from "./params";
import * as server from "./server";
import './scss/PreProcessing.scss'
import {useStepHook} from "../../../sammie/js/modules/modulehooks";
import ErrorHint from "../../../sammie/js/ui/elements/ErrorHint";
import {EelResponse} from "../../../sammie/js/eel/eel";
import {PipelineImage} from "../../../sammie/js/types/datatypes";
import {useState} from "react";

/**PERSISTENT UI STATE DEFINITIONS*/
const asFlippedImage = atomFamily<PipelineImage,string>({key:'pre-processing_demo',default:null});
const asLastRunSettings = atomFamily< {inputs:self.Inputs, params:self.Parameters},string>({key:'pre-processing_initial',default:null});

interface IPreProcessingProps{}
const PreProcessing:React.FC<IPreProcessingProps> = () => {
    
    /**CLEANUP CALLBACK WHEN INPUTS HAVE CHANGED*/
    const onInputChanged = ()=>{
        setFlippedImage(null)
    };
    
    /**RUNNING ALGORITHM CALLBACK*/
    const runMainAlgorithm = async (params:self.Parameters,step:self.Step)=>{
        const res = await server.runPreProcessing(params,step);
        setError(res.error ? res : null)
        setFlippedImage(res.error ? null : res.data.resultingImage)
        
        return res.error ? {error:res.error} : true;
    };
    
    /**CORE HOOK FOR SETTING UP STATE*/
    const {curInputs,curStep,curParams,isRunning,curBatch} = useStepHook<self.Inputs, self.Parameters,self.Step>(asLastRunSettings,
        onInputChanged,
        runMainAlgorithm,
        {msg: 'Running PreProcessing', display: "overlay"});
    
    /**UI SPECIFIC STATE*/
    const [flippedImage,setFlippedImage] = useRecoilState(asFlippedImage(curStep.moduleID))
    const [error,setError] = useState<EelResponse<any>>(null)
    
	return (<div className={'pre-processing'}>
	    {error && <ErrorHint error={error}/> }
        {!error && flippedImage &&
            <>
                <img src={flippedImage.url} />
            </>
        }
	</div>);
}
export default PreProcessing