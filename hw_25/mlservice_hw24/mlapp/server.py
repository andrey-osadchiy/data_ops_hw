from pathlib import Path
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette_exporter import PrometheusMiddleware, handle_metrics

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "diabets_model.pkl"

app = FastAPI(title="Diabets ML Service", version="1.0.0")
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

_model = None

class PatientFeatures(BaseModel):
    age: float = Field(..., description="Patient age")
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

    def to_row(self):
        return [[
            self.age, self.sex, self.bmi, self.bp, self.s1,
            self.s2, self.s3, self.s4, self.s5, self.s6
        ]]

@app.on_event("startup")
def load_model():
    global _model
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    else:
        _model = None

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": _model is not None}

@app.post("/api/v1/predict")
def predict(payload: PatientFeatures):
    if _model is None:
        return {"predict": 154.55}
    value = float(_model.predict(payload.to_row())[0])
    return {"predict": value}