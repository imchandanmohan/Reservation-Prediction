import streamlit as st
import calendar
import numpy as np
import joblib
import sys
from pathlib import Path

# --- Project imports ---
sys.path.append(str(Path(__file__).resolve().parents[1]))
from config.paths_config import MODEL_OUTPUT_PATH
from src.logger import get_logger
from src.custom_exception import CustomException

# ---------- Setup ---------- #
logger = get_logger(__name__)

st.set_page_config(
    page_title="Hotel Cancellation Predictor ❤️",
    page_icon="🏨",
    layout="wide",
)

# ---------- Custom CSS ---------- #
# Global style + utility classes for cards & buttons
st.markdown(
    """
    <style>
    ...
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ---------- #
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This demo predicts whether a hotel booking will be **cancelled** or **confirmed** based on reservation details.")
    st.divider()
    st.write("👨‍💻 Built with Streamlit.")
    st.caption("Version 1.1 – UI refresh ✨")

# ---------- Load model ---------- #
# Convert MODEL_OUTPUT_PATH to Path, if needed
if isinstance(MODEL_OUTPUT_PATH, str):
    MODEL_OUTPUT_PATH = Path(MODEL_OUTPUT_PATH)

absolute_path = MODEL_OUTPUT_PATH.resolve()
logger.info(f"🔍 Checking model path: {absolute_path}")

model = None
if not absolute_path.exists():
    logger.error(f"❌ Model file not found at: {absolute_path}")
else:
    try:
        model = joblib.load(absolute_path)
        logger.info("✅ Model loaded successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        model = None

# ---------- Page Heading ---------- #
st.markdown("""
<div style="text-align:center; margin-bottom:2rem;">
    <h1 style="font-size:2.75rem; margin-bottom:.25rem;">🏨 Hotel Cancellation Predictor</h1>
    <p style="font-size:1.15rem; color:#555;">Enter booking details to find out if a reservation is likely to be cancelled.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Input Form ---------- #
with st.container():
    with st.form("reservation_form"):
        st.markdown("<div class='form-box'>", unsafe_allow_html=True)
        st.subheader("Reservation Details")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            lead_time = st.number_input("Lead Time (days)", 0, 365, 30)
            no_of_special_requests = st.number_input("Special Requests", 0, step=1)
            market_segments = ["Aviation", "Complimentary", "Corporate", "Offline", "Online"]
            market_segment_type_label = st.selectbox("Market Segment", market_segments)
            market_segment_type = market_segments.index(market_segment_type_label)
        
        with col2:
            arrival_month = st.selectbox("Arrival Month", list(range(1, 13)), format_func=lambda m: calendar.month_name[m])
            arrival_date = st.selectbox("Arrival Day", list(range(1, 32)))
            type_of_meal_plan_label = st.selectbox("Meal Plan", ["Meal Plan 1", "Meal Plan 2", "Meal Plan 3", "Not Selected"])
            type_of_meal_plan = ["Meal Plan 1", "Meal Plan 2", "Meal Plan 3", "Not Selected"].index(type_of_meal_plan_label)
        
        with col3:
            avg_price_per_room = st.number_input("Avg. Price per Room (₹)", 0.0, step=50.0, format="%.2f")
            no_of_week_nights = st.number_input("Week Nights", 0, step=1)
            no_of_weekend_nights = st.number_input("Weekend Nights", 0, step=1)
            room_type_reserved_label = st.selectbox("Room Type", [f"Room Type {i}" for i in range(1, 8)])
            room_type_reserved = [f"Room Type {i}" for i in range(1, 8)].index(room_type_reserved_label)

        submitted = st.form_submit_button("Predict")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Prediction ---------- #
if submitted:
    import pandas as pd

    columns = [
        "lead_time",
        "no_of_special_requests",
        "avg_price_per_room",
        "arrival_month",
        "arrival_date",
        "market_segment_type",
        "no_of_week_nights",
        "no_of_weekend_nights",
        "type_of_meal_plan",
        "room_type_reserved"
    ]

    data = [[
        lead_time,
        no_of_special_requests,
        avg_price_per_room,
        arrival_month,
        arrival_date,
        market_segment_type,
        no_of_week_nights,
        no_of_weekend_nights,
        type_of_meal_plan,
        room_type_reserved
    ]]

    df = pd.DataFrame(data, columns=columns)


    try:
        if model is None:
            st.warning("⚠️ Model not available – using fallback logic.")
            prediction = 1 if lead_time < 30 else 0
        else:
            prediction = model.predict(df)[0]
            logger.info("✅ Prediction successful.")

        # ---- Display result ---- #
        if prediction == 0:
            st.markdown(
                f"<div class='metric-card metric-error'>🚫 <strong>Likely to Cancel</strong></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='metric-card metric-success'>✅ <strong>Booking Confirmed</strong></div>",
                unsafe_allow_html=True,
            )

        with st.expander("🔍 Feature Summary"):
            st.json({
                "lead_time": lead_time,
                "special_requests": no_of_special_requests,
                "avg_price_per_room": avg_price_per_room,
                "arrival_month": arrival_month,
                "arrival_date": arrival_date,
                "market_segment_type": market_segment_type_label,
                "week_nights": no_of_week_nights,
                "weekend_nights": no_of_weekend_nights,
                "meal_plan": type_of_meal_plan_label,
                "room_type_reserved": room_type_reserved_label,
            })

    except Exception as e:
        st.error(f"Prediction failed: {e}")
        logger.error(f"❌ Prediction error: {e}")
        raise CustomException("Model prediction failed", e)

# ---------- Debug Info ---------- #
with st.sidebar:
    with st.expander("🛠 Debug Info"):
        st.code(f"Model path: {absolute_path}")
        st.code(f"Model loaded: {model is not None}")
