from flask import Blueprint,request,jsonify,Flask
from models.model import CharacterLevelCNN
from models.model import get_model_params
from models import _predict_sentiment
import db 
app = Flask(__name__)
api = Blueprint('api',__name__)

model_name = 'model_en.pth'
model_path = f'./models/{model_name}'
model = CharacterLevelCNN(args = {drop_input:0})




@api.route('/predict',methods=['POST'])
def predict_sentiment():
    '''Endpoint to predict rating sentiment'''
    if request.method == 'POST':
        if 'review' not in request.form:
            return jsonify({'error':'no review in body'}),400
        else:
            parameter = get_model_params()
            review = request.form['review']
            output = _predict_sentiment(model,review,**parameter)
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
    if any(field not in request.form for field in expected_fields):
        return jsonify({'error':'Something missing in the fields'}),400
    query = db.Review.create(**request.form)
    return jsonify(query.serialize())

@api.route('/reviews',methods=['GET'])
def get_reviews():
    '''Fetch reviews'''
    if request.method=='GET':
        query = db.Review.select()
        return jsonify([ret.serialize for ret in query])
