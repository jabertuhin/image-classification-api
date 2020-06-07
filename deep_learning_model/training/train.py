import torch
import pytorch_lightning as pl

from deep_learning_model.training.models import Classifier
from deep_learning_model.training import config

model = Classifier()
trainer = pl.Trainer(max_epochs=50, gpus=1)

trainer.fit(model)
torch.save(model.state_dict(), config.MODEL_NAME)
trainer.test(model)