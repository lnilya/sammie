import json
from typing import Optional

import imageio

from src.py.loaders.fileloaderutil import __normImage
from src.sammie.py.ModuleConnector import LoaderResult
from src.sammie.py.util.imgutil import getPreviewImage


def loadIntensityImage(asPreviewOnly:bool, pipekey:str, filePath:str, **normalizationParams)->Optional[LoaderResult]:
    """Loads a grayscale image as normalized 0-1 numpy array. For Demo purposes of the demo pipeline."""

    print('[loadIntensityImage]: %s from %s' % (pipekey, filePath))

    rdr = imageio.get_reader(filePath)
    meta = rdr.get_meta_data()
    if meta is not None and 'description' in meta:
        meta = json.loads(meta['description'])
    else:
        meta = {}

    g = rdr.get_data(0)
    if len(g.shape) == 3:  g = g[:,:,0];
    # g = imageio.imread(filePath, as_gray=True)
    g = __normImage(g, **normalizationParams)
    preview = getPreviewImage(g,pipekey)

    retMeta = {'Width':g.shape[1],'Height':g.shape[0]};

    return LoaderResult(g,preview['url'],retMeta)

