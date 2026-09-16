
import streamlit as st
import pandas as pd
import joblib


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Telco Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# Load Model
# -----------------------------

@st.cache_resource
def load_model():
    return joblib.load("churn_prediction_pipeline.pkl")


model = load_model()


# -----------------------------
# App Title
# -----------------------------

st.title("📊 Telco Customer Churn Prediction")

st.write(
    "Enter customer details to predict the probability of churn."
)


# -----------------------------
# Customer Input
# -----------------------------

col1, col2 = st.columns(2)


with col1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        ["No", "Yes"]
    )

    partner = st.selectbox(
        "Partner",
        ["No", "Yes"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["No", "Yes"]
    )

    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        max_value=72,
        value=12
    )

    phone_service = st.selectbox(
        "Phone Service",
        ["No", "Yes"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["No phone service", "No", "Yes"]
    )

    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    online_security = st.selectbox(
        "Online Security",
        ["No", "Yes", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["No", "Yes", "No internet service"]
    )


with col2:

    device_protection = st.selectbox(
        "Device Protection",
        ["No", "Yes", "No internet service"]
    )

    tech_support = st.selectbox(
        "Tech Support",
        ["No", "Yes", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["No", "Yes", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["No", "Yes", "No internet service"]
    )

    contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["No", "Yes"]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0
    )

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=800.0
    )


# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Churn"):

    # -----------------------------
    # Create Customer DataFrame
    # -----------------------------

    customer = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    customer_df = pd.DataFrame([customer])


    # -----------------------------
    # Convert Binary Features
    # -----------------------------

    bool_col = [
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "PhoneService",
        "PaperlessBilling"
    ]

    for col in bool_col:
        customer_df[col] = customer_df[col].map(
            {
                "Yes": 1,
                "No": 0
            }
        )


    # Gender Encoding
    # Female = 0
    # Male = 1

    customer_df["gender"] = customer_df["gender"].map(
        {
            "Male": 1,
            "Female": 0
        }
    )


    # -----------------------------
    # One-Hot Encoding
    # Match Training Encoding
    # -----------------------------

    customer_df["MultipleLines_True"] = (
        customer_df["MultipleLines"] == "Yes"
    ).astype(int)

    customer_df["MultipleLines_No phone service"] = (
        customer_df["MultipleLines"] == "No phone service"
    ).astype(int)


    customer_df["InternetService_Fiber optic"] = (
        customer_df["InternetService"] == "Fiber optic"
    ).astype(int)

    customer_df["InternetService_No"] = (
        customer_df["InternetService"] == "No"
    ).astype(int)


    # Service Features

    service_cols = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    for col in service_cols:

        customer_df[f"{col}_True"] = (
            customer_df[col] == "Yes"
        ).astype(int)

        customer_df[f"{col}_No internet service"] = (
            customer_df[col] == "No internet service"
        ).astype(int)


    # Contract

    customer_df["Contract_One year"] = (
        customer_df["Contract"] == "One year"
    ).astype(int)

    customer_df["Contract_Two year"] = (
        customer_df["Contract"] == "Two year"
    ).astype(int)


    # Payment Method

    customer_df["PaymentMethod_Credit card (automatic)"] = (
        customer_df["PaymentMethod"]
        == "Credit card (automatic)"
    ).astype(int)

    customer_df["PaymentMethod_Electronic check"] = (
        customer_df["PaymentMethod"]
        == "Electronic check"
    ).astype(int)

    customer_df["PaymentMethod_Mailed check"] = (
        customer_df["PaymentMethod"]
        == "Mailed check"
    ).astype(int)


    # -----------------------------
    # Remove Original Categorical Columns
    # -----------------------------

    customer_df = customer_df.drop(
        columns=[
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaymentMethod"
        ]
    )


    # -----------------------------
    # Feature Engineering
    # -----------------------------

    service_features = [
        "OnlineSecurity_True",
        "OnlineBackup_True",
        "DeviceProtection_True",
        "TechSupport_True",
        "StreamingTV_True",
        "StreamingMovies_True"
    ]

    customer_df["TotalServiceUsed"] = (
        customer_df[service_features].sum(axis=1)
    )


    # Average Monthly Spend

    customer_df["AvgMonthlySpend"] = 0.0

    if tenure > 0:

        customer_df["AvgMonthlySpend"] = (
            customer_df["TotalCharges"]
            / customer_df["tenure"]
        )


    # Customer Segment

    def customer_segment(x):

        if x <= 12:
            return 0

        elif x <= 36:
            return 1

        else:
            return 2


    customer_df["CustomerSegment"] = (
        customer_df["tenure"].apply(customer_segment)
    )


    # -----------------------------
    # Match Model Features
    # -----------------------------

    customer_df = customer_df.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )

    # -----------------------------
    # Prediction
    # -----------------------------

    churn_probability = model.predict_proba(
        customer_df
    )[0][1]


    # -----------------------------
    # Prediction Result
    # -----------------------------

    st.subheader("Prediction Result")

    st.metric(
        "Churn Probability",
        f"{churn_probability:.2%}"
    )


    if churn_probability > 0.50:

        st.error("⚠️ High Churn Risk")

    else:

        st.success("✅ Low Churn Risk")
