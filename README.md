# Stock Market Forecasting 📈 💸
![image](https://github.com/MuhammadAhsanBughio/Stock-Market-Forecasting/assets/139073097/41835996-63a4-4318-b8b7-d47b17f9d663)

### Project Overview 💡
Stock Market Forecasting Project 📈 Predicting Pakistan Petroleum Limited's stock prices for the next 15 days using advanced data analysis and forecasting techniques. Our LSTM model, trained on historical data, excels at capturing intricate market trends for accurate predictions.

### Data Sources 📊
The dataset was obtained by scraping data from the Pakistan Stock Exchange website using a specialized tool called PSX Data Reader. Developed by [Muhammad Amir](https://github.com/MuhammadAmir5670/psx-data-reader), this package serves as an efficient means of extracting valuable stock market information from the PSX platform.

### Tools Used 🧰
- Google Colab - Model Computation [Colab](https://colab.research.google.com/)
- Numpy
- Pandas
- Matplotlib
- Tensorflow - Sequential, Dense, LSTM
- sklearn.preprocessing - MinMaxScaler
  
### Data Cleaning/Preparation 🧹
The data contained Date | Open | High | Low | Close columns. Only the Date and Close column was selected as we were interested in the closing price of stocks only.

### Modelling 🧑🏻‍💻

#### 1. Data Preprocessing:
Imported necessary libraries for data preprocessing, including MinMaxScaler and NumPy.
Scaled the stock price data using Min-Max scaling to bring values within the range of (0, 1).

#### 2. Dataset Splitting:
Segmented the dataset into training (70%) and test (30%) sets for model evaluation.
Utilized a time step of 100 for creating input sequences.

#### 3. Model Architecture:
Constructed an LSTM (Long Short-Term Memory) model using the TensorFlow Keras API.
Configured three LSTM layers with 50 units each to capture temporal dependencies.
Added a Dense layer with 1 unit for regression output.
Compiled the model using the mean squared error loss function and the Adam optimizer.

#### 4. Model Training:
Trained the LSTM model with 100 epochs and a batch size of 64 on the training data.
Leveraged both training and test datasets for validation during the training process.

#### 5. Prediction and Performance Metrics:
Employed the trained model to make predictions on both the training and test datasets.
Inverse-transformed the predicted values to their original scale using the MinMaxScaler.
Calculated the Root Mean Squared Error (RMSE) as a performance metric.

#### 6. Model Evaluation:
Training Data RMSE (81.5): The RMSE of 81.5 on the training dataset signifies that, on average, the predicted stock prices differ from the actual values by approximately 81.5 units. This suggests that the model exhibits reasonable accuracy in capturing patterns within the training data.

Test Data RMSE (87.1): The RMSE of 87.1 on the test dataset indicates that the model's predictions align reasonably well with the actual stock prices in unseen data. Although slightly higher than the training RMSE, it remains modest, reflecting the model's effectiveness in making accurate predictions on new data.

### Future Forecast
After preprocessing the dataset with Min-Max scaling, the model was trained on historical stock prices using a rolling prediction approach with a 100-day sequence length. The iterative prediction process and subsequent visualization in a plot revealed the model's capacity to capture crucial trends. The blue line represents actual stock prices for the last 100 days, while the orange dashed line illustrates the model's forecasts for the next 15 days.

<img width="1066" alt="image" src="https://github.com/MuhammadAhsanBughio/Stock-Market-Forecasting/assets/139073097/f9dfe508-dc06-4894-b7db-24fc78ca1f70">


The forecasted results suggest a decrease in the stock price of Pakistan Petroleum Limited over the next 15 days, anticipating a decline from approximately Rs. 113 to Rs. 100. This projection provides valuable insights for investors and stakeholders, highlighting a potential shift in market dynamics. It is crucial to consider various factors that might influence these predictions, and continuous monitoring of market trends will aid in making informed decisions in response to the evolving financial landscape.

### Conclusion/Result 

- The LSTM model, trained on historical stock prices, demonstrates promising predictive capabilities, both in the training and test datasets.
- The RMSE values indicate a relatively low level of prediction error, suggesting that the model captures essential patterns in stock price movements.
- Further fine-tuning and optimization could potentially enhance the model's performance and generalization to unseen market conditions
