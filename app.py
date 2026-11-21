from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_PATH = Path(__file__).resolve().parent / "titanic_random_forest.joblib"


class Passenger(BaseModel):
    Pclass: int = Field(ge=1, le=3, description="Класс билета: 1, 2 или 3")
    Age: float | None = Field(default=None, ge=0, le=120)
    SibSp: int = Field(default=0, ge=0)
    Parch: int = Field(default=0, ge=0)
    Fare: float | None = Field(default=None, ge=0)
    Sex: str = Field(pattern="^(male|female)$")
    Embarked: str | None = Field(default=None, pattern="^(S|C|Q)$")


@lru_cache(maxsize=1)
def get_model():
    return joblib.load(MODEL_PATH)


app = FastAPI(title="Titanic ML API", version="1.0.0")


@app.get("/health")
def health():
    get_model()
    return {"status": "ok", "model": "RandomForestClassifier"}


@app.post("/predict")
def predict(passenger: Passenger):
    data = pd.DataFrame([passenger.model_dump()])
    model = get_model()
    prediction = int(model.predict(data)[0])
    probability = float(model.predict_proba(data)[0, 1])
    return {"survived": prediction, "survival_probability": round(probability, 4)}
