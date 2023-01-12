from flask import Flask, render_template, request
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pickle

app = Flask(__name__)

saved_model = pickle.load(open("saved_model.pkl", 'rb'))
ct = saved_model['pipeline']
rf = saved_model['model']
brand_encoding_dict = saved_model['brand_encoding_dict']
model_encoding_dict = saved_model['model_encoding_dict']


@app.route("/")
def index():
    conditions = [
        "Locally Used",
        "Foreign Used",
        "Brand New"
    ]

    return render_template("index.html", brands=sorted(brand_encoding_dict.keys()), models=sorted(model_encoding_dict.keys()), conditions=conditions)


@app.route("/predict", methods=['POST'])
def predict():
    form = request.form
    X_transformed = transform_input(form)
    prediction = predict_value(X_transformed)
    print(f"returning prediction :{prediction[0]}")
    return {"price": prediction[0]}


# transform_input : transforms incoming form to a format acceptable by our machine learning model
def transform_input(form):

    values = list(form.values())
    columns = form.keys()
    df = pd.DataFrame(data=[values], columns=columns)
 #   df.columns = df.columns.str.title()

    df = df.assign(
        brand_mean_encoding=df['Brand'].apply(
            lambda x: brand_encoding_dict[x]),
        model_mean_encoding=df['Model'].apply(lambda x: model_encoding_dict[x])
    )
    print(df.columns)
    print(df.values)
    return ct.transform(df)

# predict_valie: predicts the value sent to the API


def predict_value(X_transformed):
    return rf.predict(X_transformed)
