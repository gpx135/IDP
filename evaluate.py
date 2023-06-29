# -*- coding: utf-8 -*-
"""IDP Group 6

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tIuzskvxaRn1dJx0IhM8-Mhy2rpNGHAk
"""

#Import Libraries
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import resize
import os
from training_script import getUnetModel,read_stiff,class_colors

IMAGE_SIZE=128
IMAGE_CHANNELS = 38
WEIGHT_PATH="unet_model.hdf5"

classes = ['background', 'ICG', 'Blue dye', 'Specular reflection', 'Artery', 'Vein', 'Stroma', 'Artery, ICG', 'Stroma, ICG', 'Suture', 'Umbilical cord', 'Red dye']
def get_output_filename(file_path):
    directory = os.path.dirname(file_path)
    base = os.path.basename(file_path)
    file_parts = os.path.splitext(base)
    return f"{directory}/{file_parts[0]}_segmented.jpg"

def getModelWithWeights():
    model = getUnetModel(12)
    model.load_weights(WEIGHT_PATH)
    return model
def segmentation_image(file_path):
    spim, wavelength, rgb_img, metadata = read_stiff(file_path)
    resized_image = resize(spim,(IMAGE_SIZE,IMAGE_SIZE))
    test_images = np.array([resized_image])
    model = getModelWithWeights()
    test_predictions = model.predict(test_images)
    output_image = get_output_filename(file_path)
    get_output_image(test_predictions,output_image)
    return output_image

def get_output_image(test_predictions,output_file):
    test_predictions = np.argmax(test_predictions,axis=3)
    pred_classes = np.unique(test_predictions)
    segmented_image = np.zeros((IMAGE_SIZE,IMAGE_SIZE,3))
    test_predictions_reshaped = np.stack((test_predictions,)*3, axis=-1)
    predicted_class = dict()
    for pred_class in pred_classes:
      predicted_class[pred_class] = classes[pred_class]
      if pred_class != 0:
        pred_color = class_colors[pred_class]
        pred_color_rgb = [pred_class,pred_class,pred_class]
        class_masks = np.where(test_predictions_reshaped==pred_color_rgb,pred_color,[0,0,0])
        segmented_image = np.maximum(segmented_image,class_masks)
    plt.imshow(segmented_image[0])
    from matplotlib.patches import Rectangle
    handles = [
        Rectangle((0,0),1,1, color = (class_colors[index]/255)) for index in range(12)
    ]
    plt.legend(handles,predicted_class.values(),bbox_to_anchor=(1.05, 1),loc='upper left')
    print(output_file)
    plt.savefig(output_file)




