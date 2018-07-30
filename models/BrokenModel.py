import keras
from keras.layers import Input
from keras.models import Model
from .utils.cloud import remoteModel
import numpy as np

def modelOut(model, layers, index):
    device = set(layers[:index+1])
    remote = layers[index+1:]

    deviceOuts = []
    remoteIns  = []
    skipNames  = []

    for i in remote:
        rIndex = layers.index(i)
        curIn = model.layers[rIndex].input
        for j in device:
            dIndex = layers.index(j)
            out = model.layers[dIndex].output
            if curIn==out:
                d = model.layers[index].output
                r = Input(out.shape[1:])
                deviceOuts.append(out)
                remoteIns.append(r)
                skipNames.append(model.layers[dIndex].name)

    return deviceOuts, remoteIns, skipNames

class BrokenModel(object):
    """Can split the model at the given layer into two parts.
    """
    def __init__(self, model, splitLayer, custom_objects):
        """
        # Arguments
            model: keras model to be split
            splitLayer: layer to split the model at
        """
        super(BrokenModel, self).__init__()
        self.model      = model
        self.layers     = [i.name for i in self.model.layers]
        self.splitLayer = splitLayer
        self.layerLoc   = self.layers.index(self.splitLayer)
        self.custom_objects = custom_objects

    def splitModel(self):
        """Splits the given keras model at the specified layer.
        """
        deviceOuts, remoteIns, skipNames = modelOut(self.model, self.layers, self.layerLoc)

        self.deviceModel = Model(inputs=self.model.input, outputs=deviceOuts)
        self.remoteModel = remoteModel(self.model, self.splitLayer, self.custom_objects)
