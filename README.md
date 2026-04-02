🌍 UK National Emissions Forecasting (2005–2023)
Time Series Forecasting using ARIMA & Prophet | Databricks | Python | Streamlit App
This project demonstrates an end to end time series forecasting pipeline built using Databricks, Python, ARIMA, Prophet, and Streamlit, based on UK national greenhouse gas emissions data (2005–2023). 
It showcases practical skills in statistical modelling, ML engineering, cloud analytics and deployment — aligned with real enterprise use cases in sustainability, utilities, and public sector analytics.
Project Overview
The goal of this project is to forecast UK greenhouse gas emissions for the next 10 years using classical and modern time series models. 
The pipeline includes:
A) Data ingestion & cleaning
•	Time series diagnostics (ADF, ACF, PACF)
•	Model development (ARIMA, Prophet)
•	Model comparison
•	Forecast visualization
•	Deployment via Streamlit chatbot
•	Integration-ready output for SAP Datasphere / SAC
This mirrors how forecasting is done in Fortune 500 and Big 4 consulting environments.
B) Dataset
Source: UK Government GHG Emissions Dataset (2005–2023) 
Granularity: National-level annual emissions 
Sectors: Transport, CO₂, and other greenhouse gases
The dataset was processed using Spark in Databricks and exported for modelling.
Techniques & Statistical Methods Used
C) Time Series Diagnostics
•	ADF Test — stationarity check
•	ACF Plot — autocorrelation structure
•	PACF Plot — partial autocorrelation
•	Seasonal Decomposition — trend, seasonality, residuals
D) Model Development
•	ARIMA / SARIMA
o	Manual tuning
o	Grid search over (p, d, q)
o	Residual analysis
•	Prophet
o	Trend modelling
o	Uncertainty intervals
o	Future dataframe generation
E) Model Evaluation
•	Train/test split
•	RMSE comparison
•	Visual forecast comparison
•	Stability & trend analysis
F) Architecture:
Databricks (Spark) → Python ML (ARIMA/Prophet) → Forecast Output
        ↓
   Streamlit App (Chatbot UI)
        ↓
Optional: Push predictions to SAP Datasphere → SAC Dashboard
This architecture mirrors modern SAP + Cloud + ML analytics pipelines.
G) Deployment
A fully interactive Streamlit chatbot application was built to allow users to:
•	Query historical emissions
•	View ARIMA forecasts
•	View Prophet forecasts
•	Compare models
•	Explore future predictions (2024–2033)
The app is deployed publicly and accessible online.
H) Technologies Used
•	Python
•	Databricks (Spark)
•	Pandas, NumPy
•	Statsmodels (ARIMA, ADF, ACF, PACF)
•	Prophet
•	Matplotlib / Seaborn
•	Streamlit
•	GitHub for version control
I) Key Results
•	Built accurate 10 year forecasts for UK Transport and CO₂ emissions
•	ARIMA provided stable trend-based predictions
•	Prophet captured long-term trend shifts
•	Combined insights delivered a robust forecasting view
•	Deployed a chatbot interface for interactive exploration




