import boto3
import numpy as np
from botocore.client import Config
from flask import Flask, jsonify, request
from flask_cors import CORS
from gtts import gTTS
from twilio.rest import Client

from config import ACCESS_KEY_ID, ACCESS_SECRET_KEY, BUCKET_NAME, config
from crop_recommendation.corp_prediction import recommend_crop
from crop_recommendation.weather import weather_fetch
from disease_classifier.classify_disease import predict_image
from farmers_log.search_user_request import search_log
from fertilizier_predict.crop_type_encoder import encode_crop_type
from fertilizier_predict.decode_fertilizer import decode_fertilizer
from fertilizier_predict.fertilizer_report import generate_fertilizer_report
from fertilizier_predict.min_max import min_max
from fertilizier_predict.predict_fertilier import recommend_fertilizer
from fertilizier_predict.soil_type_encoder import encode_soil_type
from localization.translator import translate_text_to_language
from utils import response_payload
from ai.call import call_voice


    
app = Flask(__name__)
CORS(app)


#The thelephone number associated whit the twilio account is: 
# --------> +240222313788
# The titles of the topics stored in the database are:
    # Nutrition
    # Fertilizantes
    # Cultivation
    # Harvest

@app.route("/test", methods = ["GET"])
def test():
    return response_payload(True, "Hello World")

@app.route("/search/<body>", methods = ["GET"])
def search(body):
    body = "solution for "+ body
    resp = farmers_log(query = {"log":body,  "lang":"en"})
    response = resp["data"]["organic_result_1"]["response"]
    if(response == ""):
        response = "Sorry, we could not find any solution for your problem"
    return response_payload(True,{
        "response":response
    } ,"Working")

@app.route("/farmers-log", methods = ["POST"])
def farmers_log(query = None):
    if query == None:
        data, form_valid = check_form_data()
    else:
        data,form_valid = query, 1
    if form_valid == 0:
        return response_payload(False, msg= data)
    log = data.get("log")
    lang = data.get("lang")
    print('Log is : ', log)
    if lang == None:
        lang = "en"
    if not log:
        return response_payload(False, msg="No log provided")
    search_result = search_log(log,lang)
    return response_payload(True,search_result, "Success search")


def check_form_data():
    try:
        data = request.get_json()
        valid = 1
    except Exception:
        data = "Request body could not be found"
        valid = 0
    if not data:
        valid = 0
        data = "No data provided"
    return data, valid


@app.route('/crop-recommedation', methods = ["POST"])
def crop_recommedation():
    
    data, form_valid = check_form_data()
    if form_valid == 0:
        return response_payload(False, msg= data)
    
    try:
        N = int(data.get('nitrogen'))
        P = int(data.get('phosphorous'))
        K = int(data.get('pottasium'))
        ph = float(data.get('ph'))
        rainfall = float(data.get('rainfall'))
        city = data.get("city")
        lang = data.get("lang")
        
        if lang == None:
            lang = "en"
        city = translate_text_to_language(city, "en", lang)
        

        try:
            city_info = weather_fetch(city)
            
        except Exception:
            return response_payload(False, msg="Unable to get the city information. Please try again")
         
        if city_info != None:
            temperature, humidity = city_info
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            
            my_prediction = recommend_crop(data)
            app.logger.info("This is the prediction"+my_prediction)
            recommendation_result = {
                    "prediction": translate_text_to_language(my_prediction[0],lang, "en")
                }
            return response_payload(True, recommendation_result, "Success search")
        else:
            return response_payload(False, 'Please try again') 
        
    except Exception:
        return response_payload(False, msg="Request body is not valid")
    
    
@app.route('/fertilizer-predict', methods = ["POST"])
def predict_fertilizer():
    data, form_valid = check_form_data()
    if form_valid == 0:
        return response_payload(False, msg= data)
    
    try:
        soil_type = str(data.get('soil-type'))
        crop_type = str(data.get('crop-type'))
        moisture = data.get('moisture')
        N = int(data.get('nitrogen'))
        P = int(data.get('phosphorous'))
        K = int(data.get('pottasium'))
        city = data.get("city")
        lang = data.get("lang")
        if lang == None:
            lang = "en"
        app.logger.info(soil_type)
        soil_type = translate_text_to_language(soil_type, "en", lang)
        crop_type = translate_text_to_language(crop_type, "en", lang)
        city = translate_text_to_language(city, "en", lang)
        
        try:
            city_info = weather_fetch(city)
        except Exception:
            return response_payload(False, msg="Unable to get the city information. Please try again")
        
        encoded_soil_type = encode_soil_type(soil_type)
        encoded_crop_type = encode_crop_type(crop_type)
        app.logger.info(encoded_crop_type)
        
        if(encoded_soil_type == None and encoded_crop_type == None):
            return response_payload(False, msg="Invalid soil type or crop type")
        
        if city_info != None:
            temperature, humidity = city_info
            data = np.array([[ temperature , humidity , moisture,encoded_soil_type,encoded_crop_type, N, P, K]])
            app.logger.info(data)
            try:
                data = min_max(data)
                print('Data ', data)
            except  Exception as e:
                print('Error')
                print(e)
                
            try:
                my_prediction = recommend_fertilizer(data)
            except  Exception as e:
                print('Error')
                print(e)
            prediction = decode_fertilizer(my_prediction[0])
            recommendation_result = {
                    "prediction": prediction,
                    "info":  generate_fertilizer_report(prediction, lang)
                }
            return response_payload(True, recommendation_result, "Success prediction")
        else:
            return response_payload(False, 'Please try again') 
        
    except Exception as e:
        print(e)
        return response_payload(False, msg="Request body is not valid")

@app.route('/find_response/<lang>/<message_body>', methods=['GET','POST'])
def find_response(message_body, lang):
    try:
        call_voice(message_body)
        return response_payload(True,'Calling User.....', 'Succesful sent')
    except Exception as ex:
        print(ex)
        return jsonify({'message':"Error"})



@app.route('/disease-predict/<lang>', methods=['GET', 'POST'])
def disease_prediction(lang):
    if request.method == 'POST':
        if lang == None:
            lang = "en"

        if 'file' not in request.files:
            return response_payload(False, 'Please select a file')
        file = request.files.get('file')
        if not file:
            return response_payload(False, 'Please select a file. Make sure there is  file')
        try:
            img = file.read()

            prediction = predict_image(img)
            recommendation_result = {
                    "prediction": translate_text_to_language(prediction, lang, "en"),
                }
            return response_payload(True, recommendation_result, "Success prediction")
            
        except Exception as e:
            print(e)
            pass
    return response_payload(False, 'Please try again')     


def page_not_found(error):
    return "<h1> Page not found ...", 404
      

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()
    
    
    