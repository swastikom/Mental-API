from functions.auxiliary_functions import predict_emotion_range, app, chatbot_ans,predict_stress

def predict_emotion(text):
    emotion = predict_emotion_range(text,
                                    '../models/Emotion Indicator Model/nlp.h5',
                                    '../models/Emotion Indicator Model/tokenizer.pkl')
    return emotion

def suicide_text_indicator(text):
    sui = app(text)
    return sui

def stress_prediction(text):
    stress = predict_stress(text)
    return stress

def chatbot_function(question):
    res = chatbot_ans(question)
    return res

def Predict_level(text):
    emo_res = predict_emotion(text)
    stress_res = stress_prediction(text)
    sui_res = suicide_text_indicator(text)

    if(emo_res == "joy"):
        return 0
    elif(emo_res == "anger"):
        if(stress_res == "this person is in stress"):
            if(sui_res == "Suicide"):
                return 8
            else:
                return 5
        else:
            return 2
    elif(emo_res == "fear"):
        if(stress_res == "this person is in stress"):
            if(sui_res == "Suicide"):
                return 9
            else:
                return 6
        else:
            return 3
    else:
        if(stress_res == "this person is in stress"):
            if(sui_res == "Suicide"):
                return 7
            else:
                return 4
        else:
            return 1
       
        
