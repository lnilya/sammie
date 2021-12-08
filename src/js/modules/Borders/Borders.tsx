import React from "react";
import {atomFamily, useRecoilState, useRecoilValue} from "recoil";
import * as alg from "../../../sammie/js/state/algstate";
import * as ui from "../../../sammie/js/state/uistates";
import * as eventbus from "../../../sammie/js/state/eventbus";
import * as self from "./params";
import * as server from "./server";
import './scss/Borders.scss'
import {useStepHook} from "../../../sammie/js/modules/modulehooks";
import ErrorHint from "../../../sammie/js/ui/elements/ErrorHint";
import {EelResponse} from "../../../sammie/js/eel/eel";
import {PipelineImage} from "../../../sammie/js/types/datatypes";
import {useState} from "react";

/**PERSISTENT UI STATE DEFINITIONS*/
const asBorderedImage = atomFamily<PipelineImage,string>({key:'borders_demo',default:null});
const asLastRunSettings = atomFamily< {inputs:self.Inputs, params:self.Parameters},string>({key:'borders_initial',default:null});

interface IBordersProps{}
const Borders:React.FC<IBordersProps> = () => {
    
    /**CLEANUP CALLBACK WHEN INPUTS HAVE CHANGED*/
    const onInputChanged = ()=>{
        setBorderedImg(null)
    };
    
    /**RUNNING ALGORITHM CALLBACK*/
    const runMainAlgorithm = async (params:self.Parameters,step:self.Step)=>{
        const res = await server.runBorders(params,step);
        setError(res.error ? res : null)
        setBorderedImg(res.error ? null : res.data)
        return res.error ? {error:res.error} : true;
    };
    
    /**CORE HOOK FOR SETTING UP STATE*/
    const {curInputs,curStep,curParams,isRunning,curBatch} = useStepHook<self.Inputs, self.Parameters,self.Step>(asLastRunSettings,
        onInputChanged,
        runMainAlgorithm,
        {msg: 'Running Borders', display: "overlay"});
    
    /**UI SPECIFIC STATE*/
    const [borderedImg,setBorderedImg] = useRecoilState(asBorderedImage(curStep.moduleID))
    const [error,setError] = useState<EelResponse<any>>(null)
    
	return (<div className={'borders'}>
	    {error && <ErrorHint error={error}/> }
        {!error && borderedImg &&
            <>
                <img src={borderedImg.url} />
            </>
        }
	</div>);
}
export default Borders