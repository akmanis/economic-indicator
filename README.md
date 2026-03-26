#Economic Indicator Dashboard

An interactive web-based dashboard to analyze and visualize key macroeconomic indicators such as GDP growth, inflation, and unemployment across countries. The project also includes correlation analysis and machine learning-based inflation prediction.

---

##Live Demo

https://economic.streamlit.app

---

## 📌 Features

* **Single Country Dashboard**

  * GDP Growth, Inflation, Unemployment trends
  * Clean and interactive time-series visualization

* **Country Comparison**

  * Compare two countries side-by-side
  * Visual comparison using line charts

* **Correlation Analysis**

  * Analyze relationship between Inflation and Unemployment
  * Helps observe economic concepts like the Phillips Curve

* **Machine Learning Prediction**

  * Linear Regression model to predict inflation
  * Forecasts next 5 years based on historical data

* **Real-time Data**

  * Data fetched from World Bank API

---

## Tech Stack

* **Frontend & App Framework:** Streamlit
* **Data Handling:** Pandas
* **Visualization:** Plotly
* **API:** World Bank API
* **Machine Learning:** Scikit-learn
* **Deployment:** Streamlit Cloud

---

## Project Structure

```
economic-dashboard/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/economic-dashboard.git
cd economic-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 📊 Data Source

* World Bank Open Data API
  https://data.worldbank.org/

---

## Key Learnings

* Handling real-world economic datasets
* Building interactive dashboards using Streamlit
* Performing correlation analysis between macro variables
* Implementing basic machine learning models for forecasting
* Deploying a data application to production

---

## Future Improvements

* Add advanced time-series models (ARIMA, LSTM)
* Include more economic indicators (interest rates, trade balance)
* Add download/export functionality
* Improve UI/UX with advanced layout

---

## 👨‍💻 Author

**Manish (AK)**

* Economics Student | Data & Fintech Enthusiast

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub and feel free to connect!

---
