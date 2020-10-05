from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn

from PIL import Image
import io
import sys
import logging

from response_dto.prediction_response_dto import PredictionResponseDto
from deep_learning_model.predictions.classify_image import ImageClassifier


app = FastAPI()

image_classifier = ImageClassifier()

@app.post("/predict/", response_model=PredictionResponseDto)
async def predict(file: UploadFile = File(...)):    
    if file.content_type.startswith('image/') is False:
        raise HTTPException(status_code=400, detail=f'File \'{file.filename}\' is not an image.')    

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')

        predicted_class = image_classifier.predict(image)
        
        logging.info(f"Predicted Class: {predicted_class}")
        return {
            "filename": file.filename, 
            "contentype": file.content_type,            
            "likely_class": predicted_class,
        }
    except Exception as error:
        logging.exception(error)
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))