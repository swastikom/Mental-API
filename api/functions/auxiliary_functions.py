import pandas as pd
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle

from sklearn.model_selection import train_test_split

# Load Functions and Model

stop_words = stopwords.words('english')
ps = PorterStemmer()

# Load Functions and Model
def load_functions_and_model(file_path):
    with open(file_path, 'rb') as f:
        saved_data = pickle.load(f)

    loaded_model = saved_data['model']

    return loaded_model

# Example usage
loaded_model = load_functions_and_model('../models/Suicide Indicator Model/sui_prediction.pkl')




def preprocess(inp):
    with open('../models/Suicide Indicator Model/tfidf.pkl', 'rb') as f:
        loaded_vectorizer = pickle.load(f)
    inp = inp.lower() #convert to lower case 
    inp = inp.replace(r'[^\w\s]+', '') #remove punctuations
    inp = [word for word in inp.split() if word not in (stop_words)] #tokenize the sentence
    inp = ' '.join([ps.stem(i) for i in inp]) #stremming
    inputToModel = loaded_vectorizer.transform([inp]).toarray() #transform to vector form
    return inputToModel

def app(input_text):
    # Define the input text box
    print('Input : ',input_text) #take input from user
    processed_array = preprocess(input_text) #preprocess the text 
    predict = loaded_model.predict(processed_array) #Model prediction
    print('Output : ', predict[0])
    return predict[0]
    

# Emotion Prediction

def predict_emotion_range(text, model_path, token_path):
    
    model = load_model(model_path)
    
    with open(token_path, 'rb') as f:
        tokenizer = pickle.load(f)
    
    sequences = tokenizer.texts_to_sequences([text])
    x_new = pad_sequences(sequences, maxlen=50)
    predictions = model.predict([x_new, x_new])
    
    emotions = {0: "anger", 1: "fear", 2: "joy", 3:"sadness"}
    
    label = list(emotions.values())
    probs = list(predictions[0])
    labels = label


    # Find the index of the maximum probability
    max_index = probs.index(max(probs))
    
    # Print the most probable emotion class
    most_probable_emotion = emotions[max_index]
    return most_probable_emotion


# Stress Prediction

def predict_stress(text):
    with open('../models/Stress Indicator Model/stress_predictor_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    with open('../models/Stress Indicator Model/tfidf_vectorizer.pkl', 'rb') as f:
        loaded_vectorizer = pickle.load(f)

    

    embedded_words = loaded_vectorizer.transform([text])
    res = loaded_model.predict(embedded_words)
    if res[0] == 1:
        res = "this person is in stress"
    else:
        res = "this person is not in stress"
    return res


# Chatbot Auxiliary Function

def chatbot_ans(q):

    nRowsRead = None 
    data = pd.read_csv('../Datasets/FAQ Chat Dataset/Mental_Health_FAQ.csv')
    data['Questions'] = data['Questions'].str.lower()
    data['Questions'] = data['Questions'].str.replace('[^\w\s]', '')
    data.dropna(inplace=True)

    
    with open('../models/FAQ Model/tfidf_vectorizer.pkl', 'rb') as f:
        loaded_vectorizer = pickle.load(f)

    user_input_vec = loaded_vectorizer.transform([q.lower()])

    with open('../models/FAQ Model/faq_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    predicted_intent = loaded_model.predict(user_input_vec)[0]
    response = data[data['Questions'] == predicted_intent]['Answers'].values[0] if predicted_intent in data['Questions'].values else "I'm sorry, I don't have a response for that question."
    
    
    return response


