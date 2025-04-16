import streamlit as st
st.set_page_config(page_title="Vehicle Transmission Predictor", layout="wide")

# ✅ Global background styling for all tabs
st.markdown(
    """
    <style>
    .stApp {
         background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
                     url("https://goauto-assets.imgix.net/RV/Go-RV-Edmonton.jpg?auto=format&ixlib=react-9.7.0&w=1075");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }
    .main > div {
        background-color: rgba(255, 255, 255, 0.93);
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# ==========================
# 📦 Load Data and Model
# ==========================
@st.cache_data
def load_readable_data():
    return pd.read_csv("df_copy_unique.csv")

@st.cache_resource
def load_balanced_data():
    X = pd.read_csv("X_train_balanced.csv")
    y = pd.read_csv("y_train_balanced.csv").squeeze()
    return X, y

@st.cache_resource
def load_model_and_encoders():
    model = joblib.load("logistic_model.pkl")
    encoders = joblib.load("label_encoders.pkl")
    return model, encoders

df = load_readable_data()
X_train_bal, y_train_bal = load_balanced_data()
model, label_encoders = load_model_and_encoders()
feature_columns = X_train_bal.columns.tolist()

# ==========================
# 🗂️ Tabs Layout
# ==========================
tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Dashboard", "🔮 Predict"])

# ==========================
# 🏠 Home Tab
# ==========================
with tab1:
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.85); padding: 30px; border-radius: 10px;">
        <h1 style="color: #FF5733;">🚗 Vehicle Transmission Prediction App</h1>
        <p style="font-size: 18px;">
            Welcome to the <span style="color: #2E86C1;"><b>Go Auto Machine Learning App</b></span>!<br><br>
            This app predicts whether a vehicle has an 
            <span style="color: #117A65;"><b>Automatic</b></span> or 
            <span style="color: #AF601A;"><b>Manual</b></span> transmission based on key vehicle attributes 
            like mileage, model, drivetrain, and more.<br><br>
            <b>Built for:</b> <span style="color: #884EA0;">Go Auto, Edmonton</span><br>
            <b>Powered by:</b> <span style="color: #CB4335;">Logistic Regression + SMOTE</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# 📊 Dashboard Tab
# ==========================
with tab2:
    st.header("📊 Interactive Power BI Dashboard")
    st.markdown("Explore the full vehicle dataset with filters and visuals.")
    st.markdown("[🔗 View Dashboard](https://your-dashboard-link.com)")  # Replace with real URL

# ==========================
# 🔮 Prediction Tab
# ==========================

# ==========================
# 🔮 Prediction Tab
# ==========================
# ==========================
# 🔮 Prediction Tab
# ==========================
with tab3:
    with st.container():
        # ✅ White box with shadow and padding only
        st.markdown("""
        <style>
            .white-box {
                background-color: rgba(255, 255, 255, 0.85);
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            }
        </style>
        <div class="white-box">
        """, unsafe_allow_html=True)

        st.header("🔧 Vehicle Input Features")

        def get_user_input():
            user_data = {}
            make = st.selectbox("Make", df["make"].unique())
            models = df[df["make"] == make]["model"].unique()
            model_name = st.selectbox("Model", models)
            series = df[(df["make"] == make) & (df["model"] == model_name)]["series"].unique()
            series_val = st.selectbox("Series", series)

            user_data["make"] = make
            user_data["model"] = model_name
            user_data["series"] = series_val

            for col in feature_columns:
                if col in ["make", "model", "series"]:
                    continue
                if df[col].dtype == 'object':
                    user_data[col] = st.selectbox(col, df[col].unique())
                else:
                    min_val, max_val = int(df[col].min()), int(df[col].max())
                    mean_val = int(df[col].mean())
                    user_data[col] = st.slider(col, min_val, max_val, mean_val)

            return pd.DataFrame([user_data])

        user_input_df = get_user_input()

        # Encode input
        encoded_input = user_input_df.copy()
        for col in label_encoders:
            if col in encoded_input.columns:
                encoded_input[col] = label_encoders[col].transform(encoded_input[col])
        for col in feature_columns:
            if col not in encoded_input.columns:
                encoded_input[col] = 0
        X_user = encoded_input[feature_columns]

        # Predict
        pred = model.predict(X_user)[0]
        pred_proba = model.predict_proba(X_user)[0]
        label = "Automatic" if pred == 1 else "Manual"

        # Output
        st.subheader("🔍 Summary of Your Input")
        st.write(user_input_df)

        st.subheader("📌 Prediction")
        st.success(f"**Predicted Transmission Type:** {label}")

        st.subheader("📈 Prediction Probability")
        st.dataframe(pd.DataFrame([pred_proba], columns=["Manual", "Automatic"]))

        # ✅ Close white box
        st.markdown("</div>", unsafe_allow_html=True)
