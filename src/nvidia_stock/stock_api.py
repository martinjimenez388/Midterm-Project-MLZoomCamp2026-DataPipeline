from fastapi import FastAPI
from typing import Dict, Any
import pickle

#Dump the model
model_file = 'RF_NVIDIA_model.bin'
with open(model_file, 'rb') as f_in:
    pipe = pickle.load(f_in)

#Define the app
app = FastAPI()

@app.post('/predict')
def predict(data: Dict[str, Any]):
    
    weekly_ret_pred = pipe.predict([data])
    close_pred = data['close'] * (1 + weekly_ret_pred[0])

    result = {
        "Predicted closing price for next week": float(close_pred),
        "Predicted weekly return": float(weekly_ret_pred[0])        
    }

    return result