import json
import pickle

from typing import List, Any

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# class DefaultData(BaseModel):
#     Category:str
#     Experience:int
#     Module:str
#     ProjectName:str
#     Technology:str

class Data(BaseModel):
    features: List[dict]


@app.post("/get_predicted_hours")
async def root(data: Data):
    convert_data = []
    for i in data.features:
        convert_data.append(list(i.values()))

    print("convert_data", convert_data)
    loaded_model = pickle.load(open('rfr_model.sav', 'rb'))
    predicted_hours_module = loaded_model.predict(convert_data)
    print("predicted_hours_module", predicted_hours_module)
    print("Total Hours", round(sum(predicted_hours_module), 2))
    response_data = json.dumps({'Total Hours': round(sum(predicted_hours_module), 2)})
    return Response(response_data)
