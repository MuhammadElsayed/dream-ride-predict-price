from flask import Flask, abort, jsonify, request, render_template
from sklearn.externals import joblib
import numpy as np
import json
import pandas as pd

gbr = joblib.load('modelxgb.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/api', methods=['POST'])
# def make_prediction():
#     data = request.get_json(force=True)
#     #convert our json to a numpy array
#     one_hot_data = input_to_one_hot(data)
#     predict_request = gbr.predict([one_hot_data])
#     output = [predict_request[0]]
#     print(data)
#     return jsonify(results=output)

def input_to_one_hot(data):
    # initialize the target vector with zero values
    enc_input = np.zeros(4)
    # set the numerical input as they are
    enc_input[0] = '2006'
    enc_input[1] = '150000'
    enc_input[2] = '25639'
    enc_input[3] = '29771'

    #enc_input[0] = data['year_model']
    #enc_input[1] = data['mileage']
    #enc_input[2] = data['make']
    #enc_input[3] = data['model']

    #enc_input[2] = data['fiscal_power']
    ##################### Mark #########################
    # # get the array of marks categories
    # marks = ['Acura', 'Alfa', 'AM', 'Aston', 'Audi', 'Bentley', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler',
    #          'Dodge', 'FIAT', 'Fisker', 'Ford', 'Freightliner', 'Genesis', 'Geo', 'GMC', 'Honda', 'HUMMER', 'Hyundai',
    #          'INFINITI', 'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Land', 'Lexus', 'Lincoln', 'Lotus', 'Maserati', 'Mazda',
    #          'Mercedes-Benz', 'Mercury', 'MINI', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Plymouth', 'Pontiac',
    #          'Porsche', 'Ram', 'Saab', 'Saturn', 'Scion', 'smart', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen',
    #          'Volvo']
    #cols = ['year_model', 'mileage', 'model', 'make']

    # redefine the the user inout to match the column name
    #redefinded_user_input = 'mark_'+data['mark']
    # search for the index in columns name list 
    #mark_column_index = cols.index(redefinded_user_input)
    #print(mark_column_index)
    # fullfill the found index with 1
    #enc_input[mark_column_index] = 1
    ##################### Fuel Type ####################
    # get the array of fuel type
    # fuel_type = ['Diesel', 'Essence', 'Electrique', 'LPG']
    # redefine the the user inout to match the column name
    # redefinded_user_input = 'fuel_type_'+data['fuel_type']
    # search for the index in columns name list 
    # fuelType_column_index = cols.index(redefinded_user_input)
    # fullfill the found index with 1
    # enc_input[fuelType_column_index] = 1
    return enc_input

@app.route('/api',methods=['POST'])
def get_delay():
    result = request.form
    year_model = result['year_model']
    mileage = result['mileage']
    make = result['mark']
    model = result['model']

    #user_input = {'Year': year_model, 'Mileage': mileage, 'MakeNum': model, 'StateNum': '0', 'ModelNum': make}
    #user_input = {'Year': year_model, 'Mileage': mileage, 'MakeNum': '25639', 'ModelNum': '29771'}

    #print(user_input)

    #a = input_to_one_hot(user_input)

    df = pd.DataFrame(columns=['Year', 'Mileage', 'MakeNum', 'ModelNum'], index=['0'])
    df.loc['0'] = pd.Series({'Year': year_model, 'Mileage': mileage, 'MakeNum': make, 'ModelNum': model})

    #df.loc['0'] = pd.Series({'Year': 2015, 'Mileage': 50000, 'MakeNum': 25639, 'ModelNum': 29771})
    #y = gbr.predict(df)

    price_pred = gbr.predict(df)

    price_pred = np.exp(price_pred)
    #price_pred = round(price_pred,2)
    return json.dumps({'price': round(price_pred[0],2)});

    # return render_template('result.html',prediction=price_pred)

if __name__ == '__main__':
    app.run(port=8080, debug=True)






