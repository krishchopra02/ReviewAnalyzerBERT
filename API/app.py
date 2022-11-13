from flask import Blueprint,request,jsonify,Flask
import sys
import os
import random

from tqdm import tqdm

import db
import config
from models.model import BERTModel 
from models._predict_sentiment import predict_sentiment
import config

app = Flask(__name__)
api = Blueprint('api',__name__)

model_name = 'model_en.pth'
model_path = f'./models/{model_name}'
model = BERTModel



@api.route('/predict',methods=['POST'])
def predict_sentiment_review():
    '''Endpoint to predict rating sentiment'''
    if request.method == 'POST':
        if 'review' not in request.form:
            return jsonify({'error':'no review in body'}),400
        else:
            parameter = get_model_params()
            review = request.form['review']
            output = predict_sentiment(model,review,**parameter)
            return jsonify(float(output))

@api.route('/review',methods=['POST'])
def post_review():
    '''ADD review to database'''
    if request.method == 'POST':
        expected_fields = [
            'review',
            'rating',
            'suggested_rating',
            'sentiment_score',
            'brand',
            'user_agent',
            'ip_address'
        ]
        print(request.form)
    if any(field not in request.form for field in expected_fields):
        return jsonify({'error':'Something missing in the fields'}),400
    query = db.Review.create(**request.form)
    return jsonify(query.serialize())

@api.route('/reviews',methods=['GET'])
def get_reviews():
    '''Fetch reviews'''
    if request.method=='GET':
        query = db.Review.select()
        return jsonify([ret.serialize() for ret in query])

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST)
