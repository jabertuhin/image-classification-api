import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader, random_split
from torchvision.datasets import CIFAR10
from pytorch_lightning.core.lightning import LightningModule

from deep_learning_model.training import config

class Classifier(LightningModule):
    def __init__(self):
        super().__init__()
        self.transform = config.TRANSFORM
        self.train_batch_size = config.TRAIN_BATCH_SIZE
        self.val_batch_size = config.VAL_BATCH_SIZE
        self.test_batch_size = config.TEST_BATCH_SIZE
        self.number_of_workers = config.NUMBER_OF_WORKERS        
        self.model = config.MODEL
        self.learning_rate = config.LEARNING_RATE
        self.model.fc = nn.Linear(in_features=self.model.fc.in_features, out_features=config.NUM_CLASSES)
        self.softmax = nn.Softmax(dim=1)        

    def forward(self, x):
        x = self.model(x)
        x = self.softmax(x)
        return x    

    def cross_entropy_loss(self, outputs, labels):        
        return nn.CrossEntropyLoss()(outputs, labels)

    def prepare_data(self):
        dataset = CIFAR10(root='./data', train=True,
                                        download=True, transform=self.transform)        
                                                
        train_set_len = int(len(dataset) * 0.9)
        val_set_len = len(dataset) - train_set_len
        self.trainset, self.valset = random_split(dataset, [train_set_len, val_set_len])                                                

        self.testset = CIFAR10(root='./data', train=False,
                                       download=True, transform=self.transform)

    def train_dataloader(self):        
        trainloader = DataLoader(self.trainset, batch_size=self.train_batch_size,
                                          shuffle=True, num_workers=self.number_of_workers)
        return trainloader                                             

    def val_dataloader(self):
        return DataLoader(self.valset, batch_size=self.val_batch_size)

    def test_dataloader(self):        
        testloader = DataLoader(self.testset, batch_size=self.test_batch_size,
                                         shuffle=False, num_workers=self.number_of_workers)                                         
        return testloader

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.cross_entropy_loss(y_hat, y)

        logs = {'train_loss': loss}
        return {'loss': loss, 'log': logs}
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.cross_entropy_loss(y_hat, y)
        return {'val_loss': loss}

    def validation_epoch_end(self, outputs):        
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        tensorboard_logs = {'val_loss': avg_loss}
        return {'avg_val_loss': avg_loss, 'log': tensorboard_logs}

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        return {'test_loss': self.cross_entropy_loss(y_hat, y)}

    def test_epoch_end(self, outputs):
        avg_loss = torch.stack([x['test_loss'] for x in outputs]).mean()
        tensorboard_logs = {'test_loss': avg_loss}
        return {'avg_test_loss': avg_loss, 'log': tensorboard_logs}

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=self.learning_rate)
        return optimizer