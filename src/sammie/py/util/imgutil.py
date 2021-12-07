import math
import os
from typing import Tuple, List, Union

import imageio
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from src.sammie.py import settings
from src.sammie.py import eelutil


# Will convert a grayscale float [0-1] image into an RGB image with the given colormap. See
# matplotlib colormaps for cmap parameter values

def norm(img: np.ndarray, range: Tuple = (0, 1), newtype=None):
    img = (img - img.min()) / (img.max() - img.min())
    img = (img + range[0]) * (range[1] - range[0])
    if newtype is not None:
        img = img.astype(newtype)

    return img

# Will retrieve the JS preview image url for a given array and key.
# will not resave if force is set to false and the preview image is already available.
def getPreviewImage(img: np.ndarray, key: str, force: bool = True):
    relPath = os.path.join(settings.TMP_FOLDER, key + '.jpg')
    absPath = eelutil.getFilePath(relPath)

    if not os.path.exists(absPath) or force:
        imageio.imsave(absPath, img)

    return {
        'url': eelutil.getFileURL(relPath, force),
        'w': img.shape[1],
        'h': img.shape[0]
    }



# Displays a number of images in a grid
def displayImageGrid(images: List, titles: List = None, dim: Tuple[int, int] = None, cmaps: Union[List, str] = None,
                     callShow: bool = False, windowTitle: str = None, fullW: bool = False, fullH: bool = False, bgCol = None,
                     **addtImshowArgs) -> List[Axes]:
    if dim is None:
        r = math.floor(math.sqrt(len(images)))
        c = math.floor(math.sqrt(len(images)))
        if (r * c < len(images)): c += 1
        if (r * c < len(images)): r += 1
        dim = (r, c)

    fig, ax = plt.subplots(dim[0], dim[1])

    if bgCol is not None:
        fig.patch.set_facecolor(bgCol)

    plt.tight_layout()
    fig.set_size_inches(18.5 if fullW else 6, 10 if fullH else 4.5)
    if windowTitle is not None:
        fig.canvas.manager.set_window_title(windowTitle)

    ax = np.ravel(ax)
    [x.axis('off') for x in ax]  # switch of all axis
    for idx, img in enumerate(images):
        if img is not None:
            if cmaps is None:
                cm = 'gray'
            elif isinstance(cmaps, str):
                cm = cmaps
            else:
                cm = cmaps[idx]
            ax[idx].imshow(img, cmap=cm, **addtImshowArgs)
            # ax[idx].imshow(img,cmap=cm)

        if titles is not None:
            ax[idx].set_title(str(titles[idx]))

    if callShow:
        plt.show()
    plt.tight_layout()
    return ax


def getPlotRowsColsForNumObj(obj: int, colsVsRows: int = 2):
    r = c = 1
    incR = colsVsRows
    # increase c colsVsRows times more often than r, so that the ratio tilts towards more columns than rows.
    while r * c < obj:
        if incR > 0:
            c += 1
            incR -= 1
        else:
            r += 1
            incR = colsVsRows

    return r, c


def setUpSubplot(rows: int = None, columns: int = None, windowTitle: str = None, axisTitles: List = None, showAxis=True,
                 fullW: bool = False, fullH: bool = False, bgCol=None) -> List[Axes]:
    fig, ax = plt.subplots(rows, columns)
    if bgCol is not None:
        fig.patch.set_facecolor(bgCol)
    if windowTitle is not None:
        fig.canvas.manager.set_window_title(windowTitle)

    # flatten axis object, makes it easier to handle
    if (rows + columns > 2):
        ax = ax.ravel()
    else:
        ax = [ax]

    # display titles if desired
    if axisTitles is not None:
        for i, a in enumerate(ax):
            if (i >= len(axisTitles)): break
            a.set_title(axisTitles[i])

    # display axises if desired
    if showAxis is False:
        [a.axis('off') for a in ax]


    elif isinstance(showAxis, list):
        for i, a in enumerate(ax):
            if showAxis[i]: continue
            a.axis('off')

    # size of widow
    fig.set_size_inches(18.5 if fullW else 6, 10 if fullH else 4.5)
    plt.tight_layout()
    return ax


def addBorder(img:np.ndarray,b,val = 0):
    bimg = np.ones((img.shape[0]+b*2,img.shape[1]+b*2),dtype=img.dtype) * val
    bimg[b:-b,b:-b] = img
    return bimg