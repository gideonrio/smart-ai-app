import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import numpy as np
import cv2
from disease_info import CLASS_NAMES

def get_model():
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(len(CLASS_NAMES), activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # In a real scenario, we would load saved weights here:
    # model.load_weights('model_weights.h5')
    
    return model

# Global model instance
model = get_model()

def prepare_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_crop_disease(image_path):
    img = prepare_image(image_path)
    preds = model.predict(img)
    class_idx = np.argmax(preds[0])
    confidence = float(np.max(preds[0]) * 100)
    return CLASS_NAMES[class_idx], confidence
