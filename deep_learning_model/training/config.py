import torchvision.transforms as transforms
from torchvision.models import resnet34

TRANSFORM = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

TRAIN_BATCH_SIZE = 32
TEST_BATCH_SIZE = 4
VAL_BATCH_SIZE = 4
MODEL = resnet34(pretrained=False) ## change it to True before training
NUM_CLASSES = 10
LEARNING_RATE = 10e-3
CLASSES = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

MODEL_NAME = 'ResNet34model.pth'