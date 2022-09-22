from flask import Flask, render_template, request
import requests
import joblib
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Current_Price = float(request.form['Current_Price'])
        Dist_Driven = np.log(int(request.form['Dist_Driven']))
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
        else:
            Fuel_Type_Diesel=1
            Fuel_Type_Petrol=0
        Year = 2020-Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        
        #Prediction
        prediction=model.predict([[Current_Price,Dist_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        
        #Output
        if(output<0):
            return render_template('index.html',prediction_text="Sorry, You cannot sell this car")
        else:
            return render_template('index.html',prediction_text="The current value of the car is {} lakhs.".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)