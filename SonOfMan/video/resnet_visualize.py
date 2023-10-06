import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.utils import model_to_dot
from sinode.sinode import Sinode as Sinode
from sinode.sinode import Node as Node

# Load the ResNet50 model
model = ResNet50(weights=None, input_shape=(224, 224, 3))

# Get the DOT representation
#dot_string = model_to_dot(model, show_shapes=True, show_layer_names=True, expand_nested=True, dpi=96).to_string()

for layer in model.layers:
    print("----")
    print(layer)
    print(layer._outbound_nodes)