import streamlit as st
import numpy as np
import cv2
from PIL import Image


image = st.file_uploader("Image Uploader", ["png", "jpg"])
image = Image.open(image).convert("RGB")
image = np.asarray(image)


# if st.button("Upload"):
#     st.session_state.image = image

# st.image(st.session_state.image)


st.image(image)
thr = st.number_input("Threshold", 0.0, 255.0, image.mean(), 1.0)
if st.button("Reset"):
    thr = image.mean()
thr_image = np.where(image > thr, 255, 0).astype(np.uint8)
st.image(thr_image)

kernal_size = st.number_input("Kernal Size", 1, 99, 3, 2)
kernal = np.ones((kernal_size, kernal_size))
st.image(cv2.erode(thr_image, kernal))


kernal_size = st.number_input("Kernal Size", 1, 99, 3, 2, key="1")
kernal = np.ones((kernal_size, kernal_size))
st.image(cv2.morphologyEx(thr_image, cv2.MORPH_GRADIENT, kernal))
