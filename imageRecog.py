import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from tensorflow.keras.applications import imagenet_utils
import os 

def detectObject(File):
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    FileName = "genna.jpg"

    model = tf.keras.applications.mobilenet_v2.MobileNetV2()
    img = image.load_img(FileName,target_size=(224,224))

    plt.imshow(img)

    resized_img = image.img_to_array(img)
    final_img = np.expand_dims(resized_img,axis=0)
    final_img = tf.keras.applications.mobilenet_v2.preprocess_input(final_img)
    final_img.shape
    predictions = model.predict(final_img)

    results = imagenet_utils.decode_predictions(predictions)
    print(results)