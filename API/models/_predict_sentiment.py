import numpy as np 
import tensorflow as tf
from model import tokenizer
def predict_sentiment(model,text,alphabet,number_of_characters,max_length,num_classes):
    tf_batch = tokenizer(pred_sentences,max_length=128,padding=True,truncation=True,return_tensors="tf")
    tf_out = model(tf_batch)
    probabilites = tf.nn.softmax(tf_outputs[0],axis=-1)
    proba,index = tf.reduce_max(probabilites, axis=1),tf.math.argmax(probabilites,axis=1)
    proba = proba.numpy().ravel()
    index = index.numpy().ravel()

    if index==0:
        score = (.33-0)*(1-proba)+0
    elif index==1:
        score = (0.67-0.33)*proba+.33 
    else:
        score=(1-.67)*proba +.67
    return score
