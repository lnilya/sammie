# SAMMIE
Scientific Algorithms Modelling and Mixing Interface Engine

Sammie allows you to easily add a browser based UI to any python based algorithms.

Internally Sammie launches a python server that communicates via a websocket with a UI built using React.JS. You can export an 
executable file for Windows or Mac OS. It presupposes a pipeline based structure where data flows from one step of the pipeline to another until the final results
are available and can be exported. Sammie also supports a batch mode, that allows to process multiple batches of data through the pipeline automatically.
Each step of the pipeline has its own parameters and set of documentations, for the users to easily and quickly grasp what each parameter is doing. 

The intention behind Sammie is to enable scientific algorithms that often come with a simple command line interface to be quickly enriched with a UI that can be exported 
as an executable file and delivered to end users.

In order to use Sammie in your project fork this repository and start developing. Please refer to the documentation to see how you can integrate your python based algorithms

For an example of how a large set of pipelines/steps and steps can be used with SAMMIE, check out [HARLEY](https://github.com/lnilya/harley). HARLEY is a software 
designed to work with yeast fluorescence microscopy images and can do a range of things through different pipelines: Detect cell outlines, Denoise fluorescence microscopy images,
train a model to detect features of interest in these images and finally batch process large sets of images using the trained model. The repository contians links to 
videos to see the software in action.

## Tech Stack

The main libraries used in SAMMIE are:

__Javascript Based__

- React and Typescript for UI development
- SASS for styling
- Recoil for state management
- Material UI for UI components
- create-react-app for development/build environment

__Python based__
- Eel / Bottle for websocket communication
- PyInstaller for creating executables

# Setting up Develompent Environment

It is much easier to use an IDE like pycharm, hence it will do most installation steps for you.

## 1. Setting Up Virtual Environment
You should have python installed. If not here is a link: https://www.python.org/downloads/release/python-382/

All the below steps assume you are in the root folder, where this readme file is located. If not open the console and type in
```
cd path/to/my/folder
```

First thing you need to do is to set up the virtual environment, which will conain
all the packages necessary for the server side of SAMMIE to run. An IDE like PYCharm will
ask you to set it up automatically, which is the easier option. To do it manually 
follow instructions below.

### For MacOS/Linux
Initialize Environment:
```
python3 -m venv venv
```
Activate Environment:
```
source venv/bin/activate
```
Upgrade Pip, optional:
```
python3 -m pip install --upgrade pip 
```
Install Required Python Packages: 
```
python3 -m pip install -r requirements.txt
```
You need to do this step only once. 

### For Windows:
Initialize environment:
```
python -m venv venv
```
Activate Environment:
```
venv\Scripts\activate.bat
```
Upgrade Pip, optional:
```
python -m pip install --upgrade pip 
```
Install Required Python Packages: 
```
python -m pip install -r requirements.txt
```
You need to do this step only once.

## 2. Starting the frontend

It is recommended that you use yarn to install the packages, because a yarn.lock file is 
included in this repository with the exact versions of the packages. You can install 
yarn globally via npm:
```
npm i -g yarn
```

Navigate to your product folder and run the installation of the packages:
```
yarn install
```
To start the JS frontend use the following script:
```
yarn start:js
```

When running in development please use port 3000, instead of 1234: http://localhost:3000. 

## 3. Starting the backend

In an IDE like PyCharm the best way is to simply debug/execute the index.py file using the buttons on the top right.
Make sure to include the "--develop" argument for development. 

A manual way is to use yarn to start the python backend for windows or mac os respectively:

#### Mac OS:
```
yarn start:py
or
python3 index.py --develop
```
#### Windows:
```
yarn startwin:py
or 
python index.py --develop
```


When not working with PyCharm or an IDE that does it for you, you might to activate the virtual environment first.

#### For MacOS/Linux
```
source .venv/bin/activate
```
#### For Windows
```
.venv\Scripts\activate.bat
```

## Helpful Links

Regarding Virtual Environments:
https://docs.python.org/3/library/venv.html

Regarding PIP packages:
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

## Caveats in current setup

### tmp folder
React-Scripts is configured to reload if any member of the public folder changes. However the tmp folder created by 
this framework will write temporary image files there, whenever they are needed. This would normally
reload the applicaiton, which is of course undesirable. To help with this, a script is used that will 
change the webpack config that is provided with react-scripts in your node-modules forlder: rswebpackfix.js.
This script is automatically prepended to the start:js command. So you do not need to deal with it explicitely. 

### eel shutdown on reload
Eel, the underlying framework fro py-js communication will shut down the process whenever all websockets are closed.
This can lead to you having to restart the py server when react is reloaded, which is terribly annoying and doesn't work with
hot reloading very well. To change this behaviour we edit the eel lab's init file, by simply disabling the _detect_shutdown function, like so: 
```
def _detect_shutdown():
    pass;
```
__You have to do this manually after installation!__ 