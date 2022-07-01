import numpy as np 
import tensorflow as tf

def predict_sentiment(model,text,alphabet,number_of_characters,max_lenght,num_classes):
    text = text.lower().strip()
    identity_mat = np.identity(number_of_characters)
    vocab = list(alphabet)
    out  = np.array([identity_mat[vocab.index(i)] for i in list(text[::-1]) if i in vocab],dtype=np.float32)
    if len(out)>max_lenght:
        out = out[:max_lenght]
    elif 0<len(out)<max_lenght:
        out  = np.concatenate((out,np.zeros(max_lenght-len(out)),number_of_characters),dtype=np.float32)
    elif len(out)==0:
        out = np.zeros((max_lenght,number_of_characters),dtype=np.float32)
    out  = tf.tensor(out)
    out = tf.expand_dims(out,axis=0)
    prediction = model(out)
    probabilites = tf.nn.softmax(prediction,axis=1)
    proba,index = tf.maximum(probabilites,axis=1)
    proba = proba.numpy().ravel()
    index = index.numpy().ravel()

    if index==0:
        score = (.33-0)*(1-proba)+0
    elif index==1:
        score = (0.67-0.33)*proba+.33 
    else:
        score(1-.67)*proba +.67
    return score