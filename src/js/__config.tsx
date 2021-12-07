import {getPipelineDefinitions} from "./pipelines/init";
import {createTheme} from "@mui/material";
import packageJson from "../../package.json";
import React, {ReactNode} from "react";


/**Main function to initialize all pipelines*/
export const pipelineDefinitions = getPipelineDefinitions;

/**A Material UI theme that governs part of the UI. Most UI is set in SCSS*/
export const theme = createTheme({
    palette: {
        primary: {
            main: '#FF7F50ff',
        },
        secondary: {
            main: '#4A5568',
        }
    },
    typography: {
        fontFamily: [
            'OpenSans',
            'sans-serif'
        ].join(','),
    },
});

/**Name for algoithm displayed in top left corner*/
export const algorithmName: string = `SAMMIE (${packageJson.version})`;

/**Logo for algoithm displayed in top left corner*/
export const algorithmLogo: ReactNode = (
    <svg width="1200pt" height="1200pt" version="1.1" viewBox="0 0 1200 1200" xmlns="http://www.w3.org/2000/svg">
        <path fill="#ffffff" d="m1140 1018.9s-71.16-28.199-105.72-44.473c-49.008-23.074-81.301-61.055-96.91-113.38-25.332-84.887-8.8906-168.41 6.9961-251.94 9.0234-47.473 19.906-94.309 12.348-143.5-24.012-156.02-117.18-262.01-249.16-337.81-124.15-71.305-284.69-77.879-413.21-14.809-80.473 39.48-400.34 285.21-123.93 745.26 43.559 62.473 248.77 232.78 318.94 228.49-103.84-94.285-179.94-421.4-179.94-421.4s106.15 370.61 322.12 471.3c-23.375-60.875-167.11-224.52-100.52-361.11 34.32-66.961 77.879-127.41 120.59-188.81 52.512-75.48 113-147.17 124.41-243.18 10.117 1.1289 13.895 7.3438 17.902 13.609 45.023 70.379 53.746 147.21 41.914 228.05-2.7227 18.613-8.5078 37.535-0.91016 56.426 44.594 110.91 9.7812 212.62-38.676 311.63-19.789 40.441-56.16 58.57-102.16 54.469-24.422-2.1719-48.793-4.5703-74.16-6.9609 169.45 145.34 520.07 18.129 520.07 18.129z"/>
    </svg>
);

/**Content of the algorithm description screen (click on logo in top left)*/
export const welcomeScreen: ReactNode = (
    <>
        <div className="text-center">
            <h1>SAMMIE Example</h1>
            <span className={'col-main'}>v. {packageJson.version}</span>
            <h4><em>S</em>cientific <em>A</em>lgorithm <em>M</em>odeling and <em>M</em>ixing <em>I</em>nterface <em>E</em>ngine</h4>
        </div>
        <div className={'pad-300-top main-text'}>
            Sammie allows you to easily add a browser based UI to any python based algorithms. The intention behind Sammie is to
            enable scientific algorithms that often come with a simple command line interface to be quickly enriched with a UI that can be exported
            as an executable file and delivered to end users.
        </div>
    </>
);