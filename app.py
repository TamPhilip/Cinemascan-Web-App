from flask import Flask, Response, request, render_template, jsonify
import re
import pickle
from keras import backend as K
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import json

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
     return render_template('main.html')

@app.route('/submit', methods = ['GET'])
def submit():
    text = request.args.get('text', "", type=str).lstrip()
    text = text.replace('\n', ' ')
    clean = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in text.lower().split("\n")]
    x = tokenize(clean)
    tags, results = predict(x)
    message = {
        'status': 200,
        'message': 'OK',
        'result': results,
        'tags': tags
    }
    toReturn = jsonify(message)
    toReturn.status_code = 200
    return toReturn

@app.route('/tokenizer')
def run_tokenizer():
    text = request.args.get('text').lstrip()
    text = text.replace('\n', ' ')
    text = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in text.lower().split("\n")]
    x = tokenize(text).tolist()
    token = {'token': x}
    return Response(json.dumps(token), mimetype='application/json')

@app.route('/predict')
def run_prediction():
    text = request.args.get('text').lstrip()
    text = text.replace('\n', ' ')
    text = [re.sub("[^a-zA-Z0-9]+", ' ', k) for k in text.lower().split("\n")]
    x = tokenize(text)
    return Response(json.dumps({'prediction': predict(x)}), mimetype='application/json')

def tokenize(text):
    with open('resources/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        sequence = tokenizer.texts_to_sequences(text)
        x = pad_sequences(sequence, maxlen=500)
        return x


def do_pred(model, genre, sequence, predictions, results):
    value = model.predict(sequence)[0][0]
    if value > 0.5:
        predictions.append(genre)
    results[genre] = str(value)
    return predictions, results


def predict(sequence):
    predictions = []
    results = {}
    genres = {
            "Action": "action_model.h5",
            "Adventure":"adventure_model.h5",
            "Comedy": "comedy_model.h5",
            "Crime": "crime_model.h5",
            "Family" : "family_model.h5",
            "Mystery" :"mystery_model.h5",
            "Romance": "romance_model.h5",
            "Thriller": "thriller_model.h5"
    }
    for genre, model_n in genres.items():
        K.clear_session()
        print("{} Loading".format(genre))
        model = load_model('./resources/n_most/{}'.format(model_n), compile=False)
        model._make_predict_function()
        predictions, results = do_pred(model, genre, sequence, predictions, results)
    print(results)
    return (predictions, results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')