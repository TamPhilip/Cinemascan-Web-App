from flask import Flask, Response, request, render_template, jsonify
import re
import pickle
from keras import backend as K
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import json

# App
app = Flask(__name__)

#  Renders the main root
@app.route('/', methods = ['GET'])
def main():
     return render_template('main.html')

# Submit the movie plot summary to be tokenized, predicted, and then return a status code of 200 okay 
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

# Specifically to tokenize the string
@app.route('/tokenizer')
def run_tokenizer():
    text = request.args.get('text').lstrip()
    text = text.replace('\n', ' ')
    text = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in text.lower().split("\n")]
    x = tokenize(text).tolist()
    token = {'token': x}
    return Response(json.dumps(token), mimetype='application/json')


# Specifically to predict the string
@app.route('/predict')
def run_prediction():
    text = request.args.get('text').lstrip()
    text = text.replace('\n', ' ')
    text = [re.sub("[^a-zA-Z0-9]+", ' ', k) for k in text.lower().split("\n")]
    x = tokenize(text)
    return Response(json.dumps({'prediction': predict(x)}), mimetype='application/json')

# Tokenize the string into a specific tokenizer
def tokenize(text):
    with open('resources/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        sequence = tokenizer.texts_to_sequences(text)
        x = pad_sequences(sequence, maxlen=500)
        return x

# Makes the prediction and gets the value from the model
def do_pred(model, genre, sequence, predictions, results):
    value = model.predict(sequence)[0][0]
    # If the value predicted is bigger than 0.5 than it has predicted it 
    if value > 0.5:
        predictions.append(genre)
    # add the value to the results
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
    # Each genre will be loaded individually to save memory
    for genre, model_n in genres.items():
        # Clears the Keras session to free up memory to decrease load time
        K.clear_session()
        print("{} Loading".format(genre))

        # Loads from one of the models
        model = load_model('./resources/n_most/{}'.format(model_n), compile=False)

        # Sets up the prediction function
        model._make_predict_function()

        # Get the value from the prediction and identifies if it is apart of that genre and then adds it to the results
        # And also appends the genre of the prediction
        predictions, results = do_pred(model, genre, sequence, predictions, results)

    print(results)
    return (predictions, results)

# Runs locally
if __name__ == '__main__':
    app.run(host='0.0.0.0')