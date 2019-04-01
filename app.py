from flask import Flask, Response, request, render_template
import re
from keras.preprocessing.sequence import pad_sequences
import pickle
from keras.models import load_model
import json
from tensorflow import get_default_graph

graph = get_default_graph()
action_model = load_model('resources/n_most/action_model.h5')
adventure_model = load_model('resources/n_most/adventure_model.h5')
comedy_model = load_model('resources/n_most/comedy_model.h5')
crime_model = load_model('resources/n_most/crime_model.h5')
family_model = load_model('resources/n_most/family_model.h5')
mystery_model = load_model('resources/n_most/mystery_model.h5')
romance_model = load_model('resources/n_most/romance_model.h5')
thriller_model = load_model('resources/n_most/thriller_model.h5')

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
     return render_template('main.html')

@app.route('/', methods = ['POST'])
def submit():
    text = request.form['text']
    clean = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in text.lower().split("\n")]
    x = tokenize(clean)
    tags, results = predict(x)
    return render_template("main.html", tags=tags, data=results, text=text)

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
    models = {"Action": action_model,
              "Adventure": adventure_model,
              'Comedy': comedy_model,
              "Crime": crime_model,
              "Family": family_model,
              "Mystery": mystery_model,
              "Romance": romance_model,
              "Thriller": thriller_model}
    with graph.as_default():
        predictions = []
        results = []
        for genre, model in models.items():
            value = model.predict(sequence)[0][0]
            if value > 0.5:
                predictions.append(genre)
            results.append({genre:value})
        print(results)
        return (predictions, results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
