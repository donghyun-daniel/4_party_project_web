from model import ModelTrainHandler
from model import ModelTestHandler
import pandas as pd


def ModelTrain():
    print('train start')
    RawDataFolder = 'model/raw/'
    trainmodel = ModelTrainHandler(RawDataFolder + 'train.csv')
    trainmodel.handle()
    print('train end')
def ModelTest():
    print('test start')
    testmodel = ModelTestHandler()
    testmodel.handle()
    print('test end')

# ModelTrain()
# ModelTest()
