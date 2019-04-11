from flask import Flask, Response, request, render_template, jsonify
import re
import pickle
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import json

print("Action Loading")
action_model = load_model('./resources/n_most/action_model.h5')
action_model._make_predict_function()

print("Adventure Loading")
adventure_model = load_model('./resources/n_most/adventure_model.h5')
adventure_model._make_predict_function()

print("Comedy Loading")
comedy_model = load_model('./resources/n_most/comedy_model.h5')
comedy_model._make_predict_function()

print("Crime Loading")
crime_model = load_model('./resources/n_most/crime_model.h5')
crime_model._make_predict_function()

# print("Family Loading")
# family_model = load_model('./resources/n_most/family_model.h5')
# family_model._make_predict_function()
#
# print("Mystery Loading")
# mystery_model = load_model('./resources/n_most/mystery_model.h5')
# mystery_model._make_predict_function()

print("Romance Loading")
romance_model = load_model('./resources/n_most/romance_model.h5')
romance_model._make_predict_function()

print("Thriller Loading")
thriller_model = load_model('./resources/n_most/thriller_model.h5')
thriller_model._make_predict_function()

print("Done Loading")
# models = {"Action": action_model,
          # "Adventure": adventure_model,
          # 'Comedy': comedy_model,
          # "Crime": crime_model,
#           "Family": family_model,
#           "Mystery": mystery_model,
#           "Romance": romance_model
#           "Thriller": thriller_model
#             }
#
# del action_model
# del adventure_model
# del comedy_model
# del crime_model
# del family_model
# del mystery_model
# del romance_model
# del thriller_model
#
# for genre, model in models.items():
#     model._make_predict_function()

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
    predictions, results = do_pred(action_model, "Action", sequence, predictions, results)
    predictions, results = do_pred(adventure_model, "Adventure", sequence, predictions, results)
    predictions, results = do_pred(comedy_model, "Comedy", sequence, predictions, results)
    predictions, results = do_pred(crime_model, "Crime", sequence, predictions, results)
    # predictions, results = do_pred(family_model, "Family", sequence, predictions, results)
    # predictions, results = do_pred(mystery_model, "Mystery", sequence, predictions, results)
    predictions, results = do_pred(romance_model, "Romance", sequence, predictions, results)
    predictions, results = do_pred(thriller_model, "Thriller", sequence, predictions, results)
    # for genre, model in models.items():
    #     if model is not None:
    #         value = model.predict(sequence)[0][0]
    #         if value > 0.5:
    #             predictions.append(genre)
    #         results[genre] = str(value)
    #     else:
    #         print("What")
    print(results)
    return (predictions, results)



if __name__ == '__main__':
    app.run(host='0.0.0.0')