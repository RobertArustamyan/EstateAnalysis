from flask import Flask, render_template, request
from joblib import load
from Functions.transform_to_nums import Transformer
from Functions.air_distance import haversine
import pandas as pd
import numpy as np

app = Flask(__name__)

YEREVAN_CENTER_LAT, YEREVAN_CENTER_LONG = 40.18111, 44.51361


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        rf_model = load('random_forest_model_apartment_sale.joblib')
        t = Transformer()

        building_type = t.transform_btype(request.form['buildingtype'])
        repair_status = t.transform_reptype(request.form['repairstatus'])
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        area = float(request.form['area'])
        floor_count = int(request.form['floorcount'])
        room_count = int(request.form['roomcount'])
        bathroom_count = int(request.form['bathroomcount'])
        balcony = t.transform_baltype(request.form['balcony'])
        elevator = t.transform_booltype(bool(request.form.get('elevator')))
        agency = t.transform_booltype(bool(request.form.get('agency')))
        covered_parking = t.transform_booltype(bool(request.form.get('coveredparking')))

        distance_from_center = haversine(YEREVAN_CENTER_LAT, YEREVAN_CENTER_LONG, latitude,longitude)

        data = pd.DataFrame({
            'agency': [agency],
            'area': [area],
            'buildingtype': [building_type],
            'elevator': [elevator],
            'floorcount': [floor_count],
            'roomcount': [room_count],
            'bathroomcount': [bathroom_count],
            'repairstatus': [repair_status],
            'balcony': [balcony],
            'distance_from_center': [distance_from_center],
            'coveredparking': [covered_parking]
        })
        prediction = np.expm1(rf_model.predict(data))
        rounded_prediction = int(prediction)

        return render_template('index.html', predicted_price=rounded_prediction)


if __name__ == '__main__':
    app.run(debug=True)
