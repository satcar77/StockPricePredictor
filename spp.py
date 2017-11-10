
import numpy
import matplotlib.pyplot as plt
import math
import warnings
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.core import Activation, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


warnings.filterwarnings("ignore")
scaler= MinMaxScaler(feature_range=(0, 1))
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

def shape_data(trainX,testX):
    trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    return trainX,testX

def normalize(dataset):
    dataset = scaler.fit_transform(dataset)
    return dataset

def build_model(l1_input_dim,l1_output_dim,hidden_dim,dropout):
    model = Sequential()
    model.add(LSTM(
        input_dim=l1_input_dim,
        output_dim=l1_output_dim,
        return_sequences=True))
    model.add(Dropout(dropout))
    model.add(LSTM(
        hidden_dim,
        return_sequences=False))
    model.add(Dropout(dropout))
    model.add(Dense(
        output_dim=1))
    model.add(Activation('linear'))
    model.compile(loss='mse', optimizer='rmsprop')
    return model

def train_model(model,trainX,trainY):
        model.fit(
        trainX,
        trainY,
        batch_size=1,
        nb_epoch=10,
        validation_split=0.05)

def predict(model,testX,number = 50): 
    points=[]
    for i in range(0,number):
        dat=model.predict(testX)
        points.append(dat[dat.shape[0]-1,dat.shape[1]-1])
        testX=numpy.reshape(dat, (dat.shape[0], 1, dat.shape[1]))
    return points

def plot(dataset,points,number): 
    arr=numpy.zeros(len(dataset)+number)
    arr[:]=numpy.nan
    p=numpy.array(points)
    final=scaler.inverse_transform([p])
    plt.plot(scaler.inverse_transform(dataset),label="Actual data")
    arr[len(dataset)-1:len(dataset)-1+number]=final[0]
    plt.plot(arr,label="Predicted data")
    print(final)
    plt.legend()
    plt.show()