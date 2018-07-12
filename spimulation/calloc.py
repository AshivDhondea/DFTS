import sys
sys.path.append('..')

from channel.gbChannel import GBC
from channel.trivialChannel import RLC
from model.quantizer import QLayer as QL

def quantInit(quantization):
    if quantization['include']:
        return QL(quantization['numberOfBits'])
    else:
        return 'noQuant'

def loadChannel(channel):
    chtype = list(channel.keys())[0]

    if chtype==0:
        return 'noChannel'
    elif chtype=='GilbertChannel':
        lp = channel[chtype]['lossProbability']
        bl = channel[chtype]['burstLength']
        return GBC(lp, bl)
    elif chtype=='RandomLossChannel':
        lp = channel[chtype]['lossProbability']
        return RLC(lp)