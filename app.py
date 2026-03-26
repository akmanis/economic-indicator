import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Economic Dashboard", layout="wide")

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Dashboard", "Comparison"])

# -----------------------------
# Country Mapping
# -----------------------------
country_dict = {
    "India": "IND",
    "USA": "USA",
    "China": "CHN",
    "Germany": "DEU",
    "UK": "GBR",
    "Japan": "JPN",
    "France": "FRA",
    "Brazil": "BRA",
    "Canada": "CAN",
    "Australia": "AUS"
}

# -----------------------------
# Indicator Mapping
# -----------------------------
indicator_dict = {
    "GDP Growth (%)": "NY.GDP.MKTP.KD.ZG",
    "Inflation (%)": "FP.CPI.TOTL.ZG",
    "Unemployment (%)": "SL.UEM.TOTL.ZS"
}

# -----------------------------
# Fetch Function (Cached)
# -----------------------------
@st.cache_data
def fetch_data(country, indicator):
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json"
    response = requests.get(url)
    data = response.json()

    if len(data) < 2:
        return None

    df = pd.DataFrame(data[1])
    if df.empty:
        return None

    df = df[['date', 'value']].dropna()
    df = df.sort_values(by='date')
    return df


# =========================================================
# 🟢 DASHBOARD (ONE COUNTRY ONLY)
# =========================================================
if page == "Dashboard":

    st.title("📊 Economic Indicator Dashboard")

    # Sidebar controls (reduces flicker feel)
    country_name = st.sidebar.selectbox("Select Country", list(country_dict.keys()), key="country1")
    indicator_name = st.sidebar.selectbox("Select Indicator", list(indicator_dict.keys()), key="indicator1")

    country = country_dict[country_name]
    indicator = indicator_dict[indicator_name]

    df = fetch_data(country, indicator)

    if df is None:
        st.error("No data available")
        st.stop()

    # Graph
    fig = px.line(df, x="date", y="value",
                  title=f"{indicator_name} - {country_name}",
                  markers=True)

    st.plotly_chart(fig, use_container_width=True)

    # Insight
    st.subheader("Insight")
    latest = df["value"].iloc[-1]

    if indicator == "NY.GDP.MKTP.KD.ZG":
        st.write("Strong growth" if latest > 6 else "Moderate/Low growth")

    elif indicator == "FP.CPI.TOTL.ZG":
        st.write("High inflation" if latest > 5 else "Moderate/Low inflation")

    elif indicator == "SL.UEM.TOTL.ZS":
        st.write("High unemployment" if latest > 6 else "Low unemployment")

    # -----------------------------
    # Correlation
    # -----------------------------
    st.markdown("---")
    st.subheader(f"Correlation ({country_name})")

    df_inf = fetch_data(country, "FP.CPI.TOTL.ZG")
    df_unemp = fetch_data(country, "SL.UEM.TOTL.ZS")

    if df_inf is not None and df_unemp is not None:
        df_inf = df_inf.rename(columns={"value": "inflation"})
        df_unemp = df_unemp.rename(columns={"value": "unemployment"})

        merged = pd.merge(df_inf, df_unemp, on="date")

        if not merged.empty:
            corr = merged["inflation"].corr(merged["unemployment"])
            st.write(f"Correlation: {round(corr, 2)}")

            fig2 = px.scatter(merged, x="inflation", y="unemployment")
            st.plotly_chart(fig2, use_container_width=True)

            # Interpretation
            if corr < -0.3:
                st.success("Negative relationship (Phillips Curve)")
            elif corr > 0.3:
                st.warning("Positive relationship (unusual)")
            else:
                st.info("Weak relationship")

    # -----------------------------
    # ML Prediction
    # -----------------------------
    st.markdown("---")
    st.subheader(f"Inflation Prediction ({country_name})")

    df_ml = fetch_data(country, "FP.CPI.TOTL.ZG")

    if df_ml is None or len(df_ml) < 15:
        st.warning("Not enough data")
    else:
        df_ml = df_ml.sort_values(by="date")
        df_ml["date"] = df_ml["date"].astype(int)

        X = df_ml["date"].values.reshape(-1, 1)
        y = df_ml["value"].values

        model = LinearRegression()
        model.fit(X, y)

        future_years = np.array(
            [df_ml["date"].max() + i for i in range(1, 6)]
        ).reshape(-1, 1)

        predictions = model.predict(future_years)

        future_df = pd.DataFrame({
            "date": future_years.flatten(),
            "value": predictions,
            "type": "Predicted"
        })

        df_ml["type"] = "Actual"
        combined = pd.concat([df_ml, future_df])

        fig3 = px.line(combined, x="date", y="value", color="type",
                       title=f"Inflation Prediction - {country_name}")

        st.plotly_chart(fig3, use_container_width=True)

        # Interpretation
        avg_pred = predictions.mean()

        if avg_pred > 5:
            st.warning("High future inflation expected")
        elif avg_pred > 2:
            st.info("Moderate inflation expected")
        else:
            st.success("Low inflation expected")


# =========================================================
# 🔵 COMPARISON PAGE
# =========================================================
elif page == "Comparison":

    st.title("🌍 Country Comparison")

    country1_name = st.sidebar.selectbox("Country 1", list(country_dict.keys()), key="c1")
    country2_name = st.sidebar.selectbox("Country 2", list(country_dict.keys()), key="c2")
    indicator_name = st.sidebar.selectbox("Indicator", list(indicator_dict.keys()), key="ind")

    country1 = country_dict[country1_name]
    country2 = country_dict[country2_name]
    indicator = indicator_dict[indicator_name]

    if country1 == country2:
        st.warning("Select different countries")
        st.stop()

    df1 = fetch_data(country1, indicator)
    df2 = fetch_data(country2, indicator)

    if df1 is None or df2 is None:
        st.error("Data not available")
        st.stop()

    df1["country"] = country1_name
    df2["country"] = country2_name

    combined = pd.concat([df1, df2])

    fig = px.line(combined, x="date", y="value", color="country",
                  title=f"{indicator_name} Comparison")

    st.plotly_chart(fig, use_container_width=True)