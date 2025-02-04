import streamlit as st
import requests

# FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/predict"

# Play type selection options
PLAY_TYPES = ["field_goal", "kickoff", "no_play", "pass", "punt", "qb_kneel", "qb_spike", "run"]

st.title("NFL Play Success Predictor")

# User Inputs
yardline_100 = st.number_input("Yardline (0-100)", min_value=0, max_value=100, value=50)
quarter_seconds_remaining = st.number_input("Quarter Seconds Remaining", min_value=0, max_value=900, value=300)
half_seconds_remaining = st.number_input("Half Seconds Remaining", min_value=0, max_value=1800, value=900)
game_seconds_remaining = st.number_input("Game Seconds Remaining", min_value=0, max_value=3600, value=1800)
quarter_end_map = {"No": 0, "Yes": 1}
quarter_end = st.selectbox("Is this the last play of the quarter?", list(quarter_end_map.keys()))
quarter_end = quarter_end_map[quarter_end]
score_differential = st.number_input("Score Differential", value=0)
drive = st.number_input("Current Drive Number", min_value=1, value=5)
down = st.number_input("Current Down (1-4)", min_value=1, max_value=4, value=1)
yards_gained = st.number_input("Yards Gained", value=0)
play_type = st.selectbox("Select Play Type", PLAY_TYPES)

if st.button("Predict Play Success"):
    # Prepare input to be fed into FastAPI
    input_data = {
        "yardline_100": yardline_100,
        "quarter_seconds_remaining": quarter_seconds_remaining,
        "half_seconds_remaining": half_seconds_remaining,
        "game_seconds_remaining": game_seconds_remaining,
        "quarter_end": quarter_end,
        "score_differential": score_differential,
        "drive": drive,
        "down": down,
        "yards_gained": yards_gained,
        "play_type": play_type
    }

    # Forward request to FastAPI
    response = requests.post(API_URL, json=input_data)

    if response.status_code == 200:
        result = response.json()
        success_probability = result["success_probability"]
        predicted_success = "Yes" if result["predicted_play_success"] else "No"

        st.subheader("Prediction Results")
        st.write(f"**Success Probability:** {success_probability * 100:.2f}%")
        st.write(f"**Predicted Play Success:** {predicted_success}")
    else:
        st.error("Error making prediction. Please try again.")
