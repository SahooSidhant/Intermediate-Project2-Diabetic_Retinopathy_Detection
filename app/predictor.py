import cv2
import numpy as np
import streamlit as st

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

IMG_SIZE = 224

CLASS_NAMES = [
    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR"
]

MODEL_PATH = r"C:\Users\iamsi\Intermediate-Project2-Diabetic_Retinopathy_Detection\models\diabetic_retinopathy_model.keras"


@st.cache_resource
def load_dr_model():
    return load_model(MODEL_PATH)


model = load_dr_model()


def predict_image(image):

    image = np.array(image)

    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))

    image = preprocess_input(image.astype(np.float32))

    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image, verbose=0)[0]

    predicted_index = np.argmax(prediction)

    predicted_class = CLASS_NAMES[predicted_index]

    confidence = float(prediction[predicted_index])

    probabilities = {
        CLASS_NAMES[i]: float(prediction[i])
        for i in range(len(CLASS_NAMES))
    }

    return predicted_class, confidence, probabilities