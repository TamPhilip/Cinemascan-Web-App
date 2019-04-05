from flask import Flask, Response, request, render_template, jsonify
import re
import pickle
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import json

action_model = load_model('resources/n_most/action_model.h5')
adventure_model = load_model('resources/n_most/adventure_model.h5')
comedy_model = load_model('resources/n_most/comedy_model.h5')
crime_model = load_model('resources/n_most/crime_model.h5')
family_model = load_model('resources/n_most/family_model.h5')
mystery_model = load_model('resources/n_most/mystery_model.h5')
romance_model = load_model('resources/n_most/romance_model.h5')
thriller_model = load_model('resources/n_most/thriller_model.h5')

models = {"Action": action_model,
          "Adventure": adventure_model,
          'Comedy': comedy_model,
          "Crime": crime_model,
          "Family": family_model,
          "Mystery": mystery_model,
          "Romance": romance_model,
          "Thriller": thriller_model}

del action_model
del adventure_model
del comedy_model
del crime_model
del family_model
del mystery_model
del romance_model
del thriller_model

for genre, model in models.items():
    model._make_predict_function()


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
     return render_template('main.html')

@app.route('/submit', methods = ['GET'])
def submit():
    text = request.args.get('text', "", type=str)
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
    text = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in text.lower().split("\n")]
    x = tokenize(text).tolist()
    token = {'token': x}
    return Response(json.dumps(token), mimetype='application/json')

@app.route('/predict')
def run_prediction():
    text = request.args.get('text')
    text = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in text.lower().split("\n")]
    x = tokenize(text)
    return Response(json.dumps({'prediction': predict(x)}), mimetype='application/json')

def tokenize(text):
    with open('resources/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        sequence = tokenizer.texts_to_sequences(text)
        x = pad_sequences(sequence, maxlen=500)
        return x

def predict(sequence):
    predictions = []
    results = {}
    for genre, model in models.items():
        if model is not None:
            value = model.predict(sequence)[0][0]
            if value > 0.5:
                predictions.append(genre)
            results[genre] = str(value)
        else:
            print("What")
    print(results)
    return (predictions, results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
