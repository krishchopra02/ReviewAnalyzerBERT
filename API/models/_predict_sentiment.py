import numpy as np 
import tensorflow as tf

def predict_sentiment(model,text,alphabet,number_of_characters,max_length,num_classes):
    text = text.lower().strip()
    identity_mat = np.identity(number_of_characters)
    vocab = list(alphabet)
    out  = np.array([identity_mat[vocab.index(i)] for i in list(text[::-1]) if i in vocab],dtype=np.float32)
    if len(out)>max_length:
        out = out[:max_length]
    elif 0<len(out)<max_length:
        out  = np.concatenate((out,np.zeros((max_length-len(out),number_of_characters),dtype=np.float32)))
    elif len(out)==0:
        out = np.zeros((max_length,number_of_characters),dtype=np.float32)
    out  = tf.constant(out)
    out = tf.expand_dims(out,axis=0)
    prediction = model(out)
    probabilites = tf.nn.softmax(prediction,axis=1)
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