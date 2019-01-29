from keras.layers import Dropout
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import Sequential
import math
import numpy
import pandas
import matplotlib.pyplot as plt
dataframe = pandas.read_csv(
    'posca_factor_ping-final.csv', usecols=[2, 3, 4, 5, 6], engine='python', skipfooter=3)
dataset = dataframe.values
dataset = dataset.astype('float32')
plt.plot(dataset)
plt.show()
seed = numpy.random.seed(7)
data_range = (-1, 1)
scaler = MinMaxScaler(feature_range=data_range)
dataset_scaled = scaler.fit_transform(dataset)
print(dataset_scaled.shape)
print(len(dataset_scaled))
print(dataset_scaled[0:10])
train_size = int(len(dataset_scaled) * 0.67)
test_size = len(dataset_scaled) - train_size
train, test = dataset_scaled[0:train_size,
                             :], dataset_scaled[train_size:len(dataset), :]
print(len(train), len(test))

def create_dataset(data, look_back=1):
    dataX, dataY = [], []
    i_range = len(data) - look_back - 1
    print(i_range)
    for i in range(0, i_range):
        dataX.append(data[i:(i + look_back)])
        dataY.append(data[i + look_back])

    return numpy.array(dataX), numpy.array(dataY)
look_back = 4
dataX, dataY = create_dataset(dataset_scaled, look_back=look_back)
print("X shape:", dataX.shape)
print("Y shape:", dataY.shape)
print("Xt-3     Xt-2      Xt-1      Xt        Y")
print("---------------------------------------------")
for i in range(len(dataX)):
    print(
        '%.2f   %.2f    %.2f    %.2f    %.2f' %
        (dataX[i][0][0],
         dataX[i][1][0],
         dataX[i][2][0],
         dataX[i][3][0],
         dataY[i][0]))
print("X shape:", dataX.shape)
dataX = numpy.reshape(dataX, (dataX.shape[0], 4, dataX.shape[2]))
print("X shape:", dataX.shape)
look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
print(trainX.shape)
print(trainY.shape)
trainX = numpy.reshape(trainX, (trainX.shape[0], look_back, trainX.shape[2]))
print("New trainX shape:", trainX.shape)
print(testX.shape)
testX = numpy.reshape(testX, (testX.shape[0], look_back, testX.shape[1]))
print("New trainX shape:", trainX.shape)
print("trainY shape:", trainY.shape)
print("trainY example:", trainY[0])
print(len(testX))
batch_size = 1
timesteps = trainX.shape[1]
input_dim = trainX.shape[2]
print(timesteps)
print(input_dim)
model = Sequential()
model.add(LSTM(4, batch_input_shape=(batch_size, timesteps, input_dim)))
model.add(Dense(10))
model.add(Dense(5))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=1000, batch_size=1, verbose=2)
trainPredict = model.predict(trainX, batch_size)
testPredict = model.predict(testX, batch_size)
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)
print("trainY shape:", trainY.shape)
print("trainPredict shape:", trainPredict.shape)
print("testY shape:", testY.shape)
print("testPredict shape:", testPredict.shape)
trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY, testPredict))
print('Test Score: %.2f RMSE' % (testScore))
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(dataset) - 1, :] = testPredict
plt.plot(scaler.inverse_transform(dataset_scaled))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()
