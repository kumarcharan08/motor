import uvicorn
from fastapi import FastAPI
import numpy as np
import pickle
from Hydraulic import Hydraulic
import pandas as pd

app = FastAPI()
pickle_in = open("motar_hydraulic.pkl","rb")
motar_hydraulic = pickle.load(pickle_in)

@app.get('/')
def index():
    return {'message': 'Hello, Sir,'}

@app.get('/{name}')
def get_name(name: str):
    return {'Welcome to my Project':f'{name}'}

@app.post('/predict')
def predict_output(data:Hydraulic):
    data = data.dict()
    PS1 = data['PS1']
    PS2 = data['PS2']
    PS3 = data['PS3']
    PS4 = data['PS4']
    PS5 = data['PS5']
    PS6 = data['PS6']
    EPS1 = data['EPS1']
    FS1 = data['FS1']
    FS2 = data['FS2']
    TS1 = data['TS1']
    TS2 = data['TS2']
    TS3 = data['TS3']
    TS4 = data['TS4']
    VS1 = data['VS1']
    CE = data['CE']
    CP = data['CP']
    SE = data['SE']
    prediction = motar_hydraulic.predict([[PS1,PS2,PS3,PS4,PS5,PS6,EPS1,FS1,FS2,TS1,TS2,TS3,TS4,VS1,CE,CP,SE]])
    output = prediction
    Cooler_Condition = output[0,0]
    if(Cooler_Condition==100):
        prediction_cooler_condition ='full efficiency'
    elif(Cooler_Condition == 20):
        prediction_cooler_condition ='close to total failure'
    else:
        prediction_cooler_condition ='Reduced efficiency'
    Valve_Condition = output[0,1]
    if (Valve_Condition == 100):
        prediction_valve_condition='optimal switching behavior'
    elif (Valve_Condition == 90):
        prediction_valve_condition='small lag'
    elif (Valve_Condition == 80):
        prediction_valve_condition='severe lag'
    else:
        prediction_valve_condition='close to total failure'
    Internal_Pump_Leakage = output[0,2]
    if (Internal_Pump_Leakage == 0):
        prediction_internal_pump_leakage='no leakage'
    elif (Internal_Pump_Leakage == 1):
        prediction_internal_pump_leakage='weak leakage'
    else:
        prediction_internal_pump_leakage='severe leakage'

    Hydraulic_Accumulator = output[0,3]
    if (Hydraulic_Accumulator == 130):
        prediction_hydraulic_accumulator='optimal switching behavior'
    elif (Hydraulic_Accumulator == 115):
        prediction_hydraulic_accumulator='small lag'
    elif (Hydraulic_Accumulator == 100):
        prediction_hydraulic_accumulator='severe lag'
    else:
        prediction_hydraulic_accumulator='close to total failure'

    Stable_Flag = output[0,4]
    if (Stable_Flag == 0):
        prediction_stable_flag='conditions were stable'
    else:
        prediction_stable_flag='static conditions might not have been reached yet'

    return {
        'prediction_cooler_condition': prediction_cooler_condition,
        'prediction_valve_condition' : prediction_valve_condition,
        'prediction_internal_pump_leakage': prediction_internal_pump_leakage,
        'prediction_hydraulic_accumulator':prediction_hydraulic_accumulator,
        'prediction_stable_flag':prediction_stable_flag
    }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)





