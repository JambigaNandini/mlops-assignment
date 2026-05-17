from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pickle
import pandas as pd

# Load model from file
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

class InputData(BaseModel):
    age: float
    education_num: float
    hours_per_week: float
    capital_gain: float
    capital_loss: float

app = FastAPI()

HTML = """<!DOCTYPE html><html><head><title>Income Predictor</title><style>body{font-family:sans-serif;background:#1a1a2e;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0}.box{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:40px;width:420px}h1{color:#00d4ff;text-align:center}p{color:#888;text-align:center;font-size:13px;margin-bottom:20px}label{color:#ccc;font-size:13px;display:block;margin-top:12px;margin-bottom:4px}input{width:100%;padding:10px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);border-radius:8px;color:white;font-size:14px;outline:none}button{width:100%;padding:13px;background:linear-gradient(90deg,#00d4ff,#0099ff);border:none;border-radius:10px;color:white;font-size:15px;font-weight:bold;cursor:pointer;margin-top:18px}.result{margin-top:20px;padding:15px;border-radius:10px;text-align:center;display:none}.high{background:rgba(0,255,150,0.1);border:1px solid #00ff96}.low{background:rgba(255,100,100,0.1);border:1px solid #ff6464}.rl{font-size:22px;font-weight:bold}.rd{font-size:12px;color:#aaa;margin-top:4px}</style></head><body><div class="box"><h1>Income Predictor</h1><p>MLOps Assignment</p><label>Age</label><input type="number" id="age" value="45"><label>Education Years</label><input type="number" id="edu" value="14"><label>Hours Per Week</label><input type="number" id="hours" value="40"><label>Capital Gain</label><input type="number" id="gain" value="5000"><label>Capital Loss</label><input type="number" id="loss" value="0"><button onclick="predict()">Predict Income</button><div class="result" id="result"><div class="rl" id="rl"></div><div class="rd" id="rd"></div></div></div><script>async function predict(){const d={age:+document.getElementById('age').value,education_num:+document.getElementById('edu').value,hours_per_week:+document.getElementById('hours').value,capital_gain:+document.getElementById('gain').value,capital_loss:+document.getElementById('loss').value};const r=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});const j=await r.json();const box=document.getElementById('result');box.style.display='block';if(j.income_above_50k){box.className='result high';document.getElementById('rl').style.color='#00ff96';document.getElementById('rl').textContent='Income > $50K';document.getElementById('rd').textContent='Earns more than $50,000/year';}else{box.className='result low';document.getElementById('rl').style.color='#ff6464';document.getElementById('rl').textContent='Income <= $50K';document.getElementById('rd').textContent='Earns $50,000/year or less';}}</script></body></html>"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML

@app.post("/predict")
def predict(data: InputData):
    df = pd.DataFrame([{
        "age": data.age,
        "education.num": data.education_num,
        "hours.per.week": data.hours_per_week,
        "capital.gain": data.capital_gain,
        "capital.loss": data.capital_loss
    }])
    prediction = model.predict(df)[0]
    label = ">50K" if prediction == 1 else "<=50K"
    return {"prediction": label, "income_above_50k": bool(prediction)}