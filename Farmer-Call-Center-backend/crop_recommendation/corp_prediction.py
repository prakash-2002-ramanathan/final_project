import pickle
import numpy as np


def recommend_crop(data):
    crop_recommendation_model_path = 'C:/Users/praka/OneDrive/Desktop/miniproj5/Farmer-Call-Center-backend/models/RandomForest.pkl'
    crop_recommendation_model = pickle.load(
        open(crop_recommendation_model_path, 'rb'))
    return crop_recommendation_model.predict(data)

#data = np.array([[40, 30, 30, 27, 40, 7, 500]])

#print("crop prediction :"+recommend_crop(data))
