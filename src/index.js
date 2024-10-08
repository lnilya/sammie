import React from 'react';
import { createRoot } from 'react-dom/client';
import './sammie/scss/index.scss';
import App from "./sammie/js/App";
import './sammie/js/eel/eelJsFunctions'
import {RecoilRoot} from "recoil";
import {SnackbarProvider} from "notistack";
import {ThemeProvider, Zoom} from "@mui/material";
import {pipelineDefinitions, theme} from "./js/__config";

window['eel']?.set_host('ws://localhost:1234');


const container = document.getElementById('root')
const root = createRoot(container)
root.render(<ThemeProvider theme={theme}>
    <RecoilRoot>
        <SnackbarProvider maxSnack={3}
                          autoHideDuration={3000}
                          TransitionComponent={Zoom} anchorOrigin={ { vertical: 'bottom', horizontal: 'right'}}>
            <App getPipelineDefinitions={pipelineDefinitions}/>
        </SnackbarProvider>
    </RecoilRoot>
</ThemeProvider>)