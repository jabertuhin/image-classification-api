from tests.conftest import test_app
import os

from PIL import Image


def test_predict_when_image_is_valid(test_app):
    # arrange             
    filepath = os.path.join('tests', 'assets', 'cat_image.jpg')     
    expected_response = {'filename': 'cat_image.jpg', 'contentype': 'image/jpeg'} ## won't check predicted class
    # act
    actual_response = test_app.post('/predict/', files={"file": ("cat_image.jpg", open(filepath, "rb"), "image/jpeg")})        
    # assert    
    assert actual_response.status_code == 200    
    actual_response = actual_response.json()
    print(actual_response)
    assert actual_response['filename'] == expected_response['filename']
    assert actual_response['contentype'] == expected_response['contentype']    

def test_predict_when_file_not_an_image(test_app):
    # arrange             
    filepath = os.path.join('tests', 'assets', 'not_image.txt')     
    expected_response = {'detail' :'File \'not_image.txt\' is not an image.'}
    # act
    actual_response = test_app.post('/predict/', files={"file":  open(filepath, "rb")})
    # assert    
    assert actual_response.status_code == 400    
    assert actual_response.json() == expected_response