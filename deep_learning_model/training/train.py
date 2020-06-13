import torch
import pytorch_lightning as pl

from deep_learning_model.training.models import Classifier
from deep_learning_model.training import config

pl.seed_everything(42)

model = Classifier()
trainer = pl.Trainer(max_epochs=50, gpus=1)

# start training
trainer.fit(model)
# save trained model
torch.save(model.state_dict(), config.MODEL_NAME)
# test on test data
trainer.test(model)