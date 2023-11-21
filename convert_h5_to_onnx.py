import keras
import onnx
from keras2onnx import convert_keras


keras_model = keras.models.load_model('path_to_your_model.h5')

# Convert Keras model to ONNX format
onnx_model = convert_keras(keras_model, 'your_model.onnx')

# Save the ONNX model
onnx.save_model(onnx_model, 'your_model.onnx')