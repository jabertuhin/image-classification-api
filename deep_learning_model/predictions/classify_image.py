from deep_learning_model.training.models import Classifier
from deep_learning_model.training.config import CLASSES, MODEL_NAME

import torch
import torchvision.transforms as transforms

import os

class ImageClassifier:
    def __init__(self):        
        self.classifier = Classifier()
        model_path = os.path.join('deep_learning_model', 'trained_model', MODEL_NAME)                 
        self.classifier.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    def predict(self, image):            
        transforms_image = transforms.Compose(
            [transforms.Resize((224, 224)),
            transforms.ToTensor(),        
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        image = transforms_image(image) 
        image = image.unsqueeze(0)

        output = self.classifier(image)    
        class_idx = torch.argmax(output, dim=1)    
        
        return CLASSES[class_idx]