
from flask import Flask,render_template,request,send_file,abort,jsonify
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,
    get_jwt_identity,verify_jwt_in_request)
import io,json 
from joblib import load
from datetime import timedelta
import pandas as pd

app = Flask(__name__)

#token manager
jwt = JWTManager(app) 

#custom function for token expiry with status code
@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


#custom function for token validation with status code
@jwt.invalid_token_loader
def my_invalid_token_callback(invalid_token):
    return jsonify({
        'status': 402,
        'msg':invalid_token
    }),402



#secret key in config file 
app.config['SECRET_KEY'] = '123456'

#port no
port = '9090'
#loading model 
model = load('./src/titanic.joblib')

#flask route 
@app.route('/')
def homepage():
    return jsonify('hello world')

#function for gender and survive analysis(Yes/No)
def gender_encoder(sex):
  return 1 if sex.lower() == 'male' else 0

def survived_endr(a):
  return 'Yes' if a==1 else 'No'  

def pred(data):
    dt = pd.DataFrame([data] )
    ot = model.predict(dt)
    survive = survived_endr(ot)
    return survive



#below code for API generate token for connecting 
#login 
@app.route('/api/v0.16/login_tk', methods = ['GET','POST'])
def login_t():
    ret = []
    key_ = request.args.get('key',None)
    uid_ = request.args.get('uid',None)
    if key_ == app.config['SECRET_KEY']:
        expires = timedelta(seconds=50)
        access_token = create_access_token(identity=uid_,expires_delta=expires)
        ret = {'access_token': access_token,'error code':200}
    else:
        ret = {'error code ':400}

    return jsonify(ret)

#api to predict the human being will survive the crash 
@app.route('/api/v0.16/clsabs', methods = ['GET','POST'])
@jwt_required
def clsfy_abst():
    current_user = get_jwt_identity() 
    Pclass = request.args.get('PClass',None)
    Sex = request.args.get('Gender',None)
    Age = request.args.get('Age',None)
    Sibsp = request.args.get('SibSp',None)
    Parch = request.args.get('Parch',None)
    Fare = request.args.get('Fare',None)
    Sex = gender_encoder(Sex)
    data = {'Pclass':Pclass,'Sex':Sex,'Age':Age,'Sibsp':Sibsp,'Parch':Parch,'Fare':Fare}
    survive = pred(data)
    result = {'survive':survive}
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)
