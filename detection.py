import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from tensorflow.keras.applications import imagenet_utils
import os 
import discord
from discord.ext import commands

async def detect(ctx, *arg):
    if arg.__len__() != 1:
        await ctx.send("Please provide one link to an image")
        return
    try: #If file cant be found or not a valid link then it will throw an error
        img_url = tf.keras.utils.get_file(None,arg)
        await ctx.send("Detecting object...")
    except:
        await ctx.send("Please provide a valid link to an image or try again")
        return

    model = tf.keras.applications.mobilenet_v2.MobileNetV2()
    img = image.load_img(img_url,target_size=(224,224))
    resized_img = image.img_to_array(img)
    final_img = np.expand_dims(resized_img,axis=0)
    final_img = tf.keras.applications.mobilenet_v2.preprocess_input(final_img)
    final_img.shape
    predictions = model.predict(final_img)

    results = imagenet_utils.decode_predictions(predictions)
    output = "This is likely a "+ results[0][0][1] + " with " + str(round(results[0][0][2]*100, 2)) + "% confidence"
    await ctx.send(output)