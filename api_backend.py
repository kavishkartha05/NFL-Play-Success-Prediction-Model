from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "nfl_data")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = FastAPI()

rf_model = joblib.load("models/best_random_forest.pkl")
expected_features = joblib.load("models/feature_names.pkl")

feature_medians = pd.read_csv("data/processed/feature_medians.csv", index_col=0).squeeze()
feature_columns = feature_medians.index.tolist()

# Defining expected input fields
class PredictionInput(BaseModel):
    yardline_100: float
    quarter_seconds_remaining: float
    half_seconds_remaining: float
    game_seconds_remaining: float
    quarter_end: int
    score_differential: float
    drive: int
    down: int
    yards_gained: float
    play_type: str

# Defining play types
PLAY_TYPES = ["play_type_field_goal", "play_type_kickoff", "play_type_no_play",
              "play_type_pass", "play_type_punt", "play_type_qb_kneel",
              "play_type_qb_spike", "play_type_run"]

def encode_play_type(play_type: str):
    """ Convert play type into a one-hot encoded dictionary. """
    play_encoding = {ptype: 0.0 for ptype in PLAY_TYPES}
    play_feature = f"play_type_{play_type.lower()}"

    if play_feature in play_encoding:
        play_encoding[play_feature] = 1.0
    else:
        raise ValueError(f"Invalid play type '{play_type}'. Choose from: {', '.join([p[10:] for p in PLAY_TYPES])}")

    return play_encoding

# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "running"}

# Prediction Endpoint
@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        input_dict = input_data.dict()

        # Converting play_type to one-hot encoding and merging
        play_type_encoding = encode_play_type(input_dict.pop("play_type"))
        input_dict.update(play_type_encoding)

        # Converting input to DataFrame and reindex to match feature order of training sets
        input_df = pd.DataFrame([input_dict])
        input_df = input_df.reindex(columns=expected_features, fill_value=0)

        # Converting input array to NumPy format for model prediction
        input_array = input_df.to_numpy()
        success_prob = rf_model.predict_proba(input_array)[0, 1]
        predicted_success = success_prob >= 0.5

        return {"success_probability": round(success_prob, 3), "predicted_play_success": bool(predicted_success)}

    except ValueError as e:
        return {"error": str(e)}  
