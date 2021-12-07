import {Parameter} from "../../../sammie/js/modules/paramtypes";
import {PipelineImage} from "../../../sammie/js/types/datatypes";
import {PipelineStep} from "../../../sammie/js/types/pipelinetypes";
import React from "react";
import {getCheckboxParams, getDropdownParams, getSliderParams} from "../../../sammie/js/modules/paramutil";

/**Name of the module*/
export const moduleName = 'PreProcessing'

/**Parameter UI Definition the user can set in PreProcessing*/
export const parameters:Array<Parameter<any>> = [
    getDropdownParams('flip','Flip Image','Allows you to flip the image. This is just an example of a dropdown','none',{none:'No Flipping',hor:'Flip Horizontally',ver:'Flip Vertically',center:'Flip Both'}),
    getCheckboxParams('thresholding','Threshold Image','Enables thresholding of the image. This is an example of a field that conditionally enables other parameters','Enable Thresholding',false),
    getSliderParams('threshold','Threshold','A slider governing the thresholding of the image. Appears only when the checkbox is set',0,1,0.01,[0.1,0.9],false,
        allSettings => allSettings['thresholding'] ? 'active' : 'hide'),
];

/**Typing for PreProcessing Inputs - Define Input Types/Names of this Pipeline step here.*/
export type Inputs = {in:PipelineImage }

/**Typing for PreProcessing Outputs - Define Output Types/Names of this Pipeline step here.*/
export type Outputs = {out:PipelineImage}

/**Shorthand for the PipelineStep of PreProcessing*/
export type Step = PipelineStep<Inputs, Outputs>;

/**Parameter Object of PreProcessing - Include all Parameters with their types that this step has. Should match the actual parameter definiton on top.*/
export type Parameters = {
    flip:boolean,
    thresholding:boolean,
    threshold:[number,number]
    //A few example data types:
}