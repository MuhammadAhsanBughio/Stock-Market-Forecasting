# -*- coding: utf-8 -*-
"""Stock_Market_Forecasting_PPL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wsKFKxxTSe23SdlX6j6X2OVD3Bu4qYrS
"""

#Installing Pakistan Stock Exchange Data Reader
!pip install psx-data-reader

# Importing Stocks and Tickers from PSX
from psx import stocks, tickers

# Getting the information of all the companies in Pakistan Stock Exchange
tickers = tickers()

"""To scrape the data of Pakistan Petrolium Limited we have passed its ticker (symbol) to the stocks method with proper start and end date. and it will return a DataFrame with the scraped data


"""

#importing datatime module
import datetime

df = stocks("PPL", start=datetime.date(2020, 1, 1), end=datetime.date.today())

import pandas as pd

df.head()

#Saving the file to CSV
df.to_csv("/content/PPL_Stock_Prices.csv", index=False)

file_path = "/content/PPL_Stock_Prices.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame
df.head()

from google.colab import files

files.download("/content/PPL_Stock_Prices.csv")

# Closing prices of the stock
df1=df.reset_index()['Close']

df1

import matplotlib.pyplot as plt

# Plotting the line
plt.plot(df1, label='Closing Price', color='blue', linestyle='-', linewidth=2)

# Adding labels and title
plt.xlabel('Days')
plt.ylabel('Closing Price')
plt.title('Stock Price Over Time')

# Adding a legend
plt.legend()

# Rotating x-axis labels for better readability
plt.xticks(rotation=45)

# Adding grid for better visualization
plt.grid(True)
# Adding background colour
plt.rcParams['axes.facecolor'] = 'aliceblue'

# Display the plot
plt.show()

"""LSTM are sensitive to the scale of the data. so we apply MinMax scaler

"""

# Importing necessary libraries
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Creating an instance of MinMaxScaler with the feature range (0, 1)
scaler = MinMaxScaler(feature_range=(0, 1))

# Reshaping the data to a single column and applying Min-Max scaling
df1 = scaler.fit_transform(np.array(df1).reshape(-1, 1))
# The scaler is fitted to the data and transforms it in one step

print(df1)

# Splitting the dataset into training and test sets
# 70% of the data for training and 30% for testing

# Calculating the index to split the data
training_size = int(len(df1) * 0.70)
test_size = len(df1) - training_size

# Slicing the data to create the training set
train_data, test_data = df1[0:training_size, :], df1[training_size:len(df1), :1]

training_size,test_size

train_data

import numpy
# Function to convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []

    # Iterate through the dataset to create input sequences and corresponding output values
    for i in range(len(dataset) - time_step - 1):
        # Input sequence (features)
        a = dataset[i:(i + time_step), 0]

        # Output value (target)
        dataY.append(dataset[i + time_step, 0])

        # Append input sequence to dataX
        dataX.append(a)

    # Convert lists to NumPy arrays for model compatibility
    return numpy.array(dataX), numpy.array(dataY)

# reshape into X=t,t+1,t+2,t+3 and Y=t+4
time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)

print(X_train.shape), print(y_train.shape)

print(X_test.shape), print(ytest.shape)

# reshape input to be [samples, time steps, features] which is required for LSTM
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

# Create the Stacked LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

# Creating a Sequential model
model = Sequential()

# Adding the first LSTM layer with 50 units, returning sequences, and specifying the input shape
model.add(LSTM(50, return_sequences=True, input_shape=(100, 1)))

# Adding a second LSTM layer with 50 units and returning sequences
model.add(LSTM(50, return_sequences=True))

# Adding a third LSTM layer with 50 units
model.add(LSTM(50))

# Adding a Dense layer with 1 unit for regression output
model.add(Dense(1))

# Compiling the model with mean squared error loss and the Adam optimizer
model.compile(loss='mean_squared_error', optimizer='adam')

model.summary()

model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=64,verbose=1)

import tensorflow as tf

tf.__version__

# Lets Do the prediction and check performance metrics
train_predict=model.predict(X_train)
test_predict=model.predict(X_test)

# Transform back to original form
train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)

# Calculate RMSE performance metrics
import math
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train,train_predict))

"""**Training Data RMSE (81.5):** This value indicates the RMSE between the predicted stock prices on the training dataset (train_predict) and the actual stock prices (y_train). An RMSE of 81.5 means that, on average, the predicted values differ from the actual values by approximately 81.5 units (or whatever units your stock prices are in). Lower RMSE values indicate better model performance, so an RMSE of 81.5 suggests that the model is relatively accurate on the training data."""

# Test Data RMSE
math.sqrt(mean_squared_error(ytest,test_predict))

"""**Test Data RMSE (87.1):** This metric signifies the Root Mean Squared Error between the predicted stock prices, as generated by the model on the test dataset (test_predict), and the actual stock prices (ytest). With an RMSE of 88, while not as low as the training dataset, the value remains relatively modest, indicating that the model's predictions align reasonably well with the actual stock prices. This suggests that the model exhibits a degree of accuracy when applied to new and unseen data, reinforcing its predictive capability."""

# Plotting
plt.rcParams['axes.facecolor'] = 'aliceblue'
plt.rc('axes',edgecolor='white')
# Shift train predictions for plotting
look_back = 100
trainPredictPlot = np.empty_like(df1)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict

# Shift test predictions for plotting
testPredictPlot = np.empty_like(df1)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(train_predict) + (look_back * 2) + 1:len(df1) - 1, :] = test_predict

# Plot baseline and predictions
plt.figure(figsize=(15, 6))  # Set the figure size for better visualization
plt.plot(scaler.inverse_transform(df1), label='Actual Stock Prices', color='blue')
plt.plot(trainPredictPlot, label='Training Predictions', color='green')
plt.plot(testPredictPlot, label='Testing Predictions', color='orange')
plt.grid(color='white')

# Add labels and title
plt.xlabel('Days')
plt.ylabel('Stock Price')
plt.title('Actual vs Predicted Stock Prices')
plt.legend()  # Add legend for better interpretation
plt.show()

len(test_data)

# Previous 100 days
x_input=test_data[213:].reshape(1,-1)
x_input.shape

# Creating a list and taking all the values from it
temp_input=list(x_input)
temp_input=temp_input[0].tolist()

temp_input

# demonstrate prediction for next 15 days
from numpy import array

lst_output=[]
n_steps=100
i=0
while(i<15):

    if(len(temp_input)>100):
        #print(temp_input)
        x_input=np.array(temp_input[1:])
        print("{} day input {}".format(i,x_input))
        x_input=x_input.reshape(1,-1)
        x_input = x_input.reshape((1, n_steps, 1))
        #print(x_input)
        yhat = model.predict(x_input, verbose=0)
        print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat[0].tolist())
        temp_input=temp_input[1:]
        #print(temp_input)
        lst_output.extend(yhat.tolist())
        i=i+1
    else:
        x_input = x_input.reshape((1, n_steps,1))
        yhat = model.predict(x_input, verbose=0)
        print(yhat[0])
        temp_input.extend(yhat[0].tolist())
        print(len(temp_input))
        lst_output.extend(yhat.tolist())
        i=i+1


print(lst_output)

"""**Logic Explained**

1. lst_output is initialized as an empty list to store the predicted values.
2. A while loop runs until 15 days of predictions are obtained.
3. Inside the loop, it checks if the length of temp_input (the input sequence) is greater than 100.
* If true, it predicts the next day's stock price based on the last 100 days of data.
* The input sequence is updated by removing the first element and adding the predicted value.
* The predicted value is added to the lst_output.
* The loop counter is incremented.
* If false, it predicts the next day's stock price based on the available data.
* The predicted value is added to temp_input.
* The loop counter is incremented.

The loop continues until 15 days of predictions are obtained. The predicted values are stored in lst_output. The model is fed with its own predictions in subsequent iterations, simulating a forecasting scenario.
"""

# previous 100 days
day_new=np.arange(1,101)
# predicted 15 days
day_pred=np.arange(101,116)

len(df1)

# Plotting
plt.figure(figsize=(12, 6))
plt.rcParams['axes.facecolor'] = 'aliceblue'
plt.grid(color='white')
plt.rc('axes',edgecolor='white')
# Actual stock prices
plt.plot(day_new, scaler.inverse_transform(df1[941:]), label='Stock Prices', color='blue', marker='o')

# Future predicted prices
plt.plot(day_pred, scaler.inverse_transform(lst_output), label='Predicted Stock Prices', linestyle='dashed', color='orange', marker='o')

# Add labels and title
plt.xlabel('Days')
plt.ylabel('Stock Price')
plt.title('15 Days Stock Price Forecast for PPL')

# Add legend
plt.legend()

# Add grid lines
plt.grid(True)

# Show the plot
plt.show()

"""The Stock Price for the next 15 days of Pakistan Petroleum Limited will decrease from Rs.115 to Rs.100 approx.

# THE END
"""

