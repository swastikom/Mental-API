from fastapi import APIRouter
from enum import Enum
import openai
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

router = APIRouter()

class Tags(Enum):
    predict_result = "Mental Health Tips based on Level"


# OpenAI Tips based on Mental Health Level Route
openai.api_key = OPENAI_API_KEY

@router.post("/query_tips", tags=[Tags.predict_result])
async def query(level: str):
    messages_chat = []
    temparature = 0.5
    max_tokens = 500

    input_prompt = """You are a mental health specialist. Now I have built a function that upon analyzing a text will give a value between a range of 0 to 9 based on the person's mental health condition. Now the text will be analyzed based on three factors. Such as,

1. Mood of the text: The possible moods are joy, sadness, anger, and fear. Based on the text we can get one among the four values.
2. Stress level: Based on the text, we can get one of the two possible values: the person is in stress and the person is not in stress.
3. Suicidal level: Based on the text, we can get one of the two possible values: the text is suicidal or non-suicidal.

Now, the value between the range 0-9 can be decided by the above 3 factors via the following combinations. Such as,

1. If the mood of the text is joy then it will give the value 0 and the person's mental health level is excellent.
2. If the mood of the text is sadness, if the stress level of the text is the person is not in stress then the value is 1. 
3. If the mood of the text is anger, if the stress level of the text is the person is not in stress then the value is 2. 
4. If the mood of the text is fear, if the stress level of the text is the person is not in stress then the value is 3. 
5. If the mood of the text is sadness, if the stress level of the text is the person is in stress and the suicidal level of the text is non suicidal then the value is 4. 
6. If the mood of the text is anger, if the stress level of the text is the person is in stress and the suicidal level of the text is non suicidal then the value is 5. 
7. If the mood of the text is fear, if the stress level of the text is the person is in stress and the suicidal level of the text is non suicidal then the value is 6. 
8. If the mood of the text is sadness, if the stress level of the text is the person is in stress and the suicidal level of the text is suicidal then the value is 7. 
9. If the mood of the text is anger, if the stress level of the text is the person is stressed and the suicidal level of the text is suicidal then the value is 8. 
10. If the mood of the text is fear, if the stress level of the text is the person is in stress and the suicidal level of the text is suicidal then the value is 9. 

Now, based on the value you have to give some tips that have the potential to improve the person's mental health conditions. while giving the tips do not say something like "This person is in ..." or "Since the mood of the text indicates..." or " value ...:" Just give a positive sentence at the beginning and give the tips with points. The introductory sentence should be positive and encouraging.

Now the value is - f"{level}" """

    messages_chat.append({"role":"user","content":f"{input_prompt}"})
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages= messages_chat,
        temperature=temparature,
        max_tokens=max_tokens,
    )

    reply = completion.choices[0].message.content
    return reply



# Mental Health Tips based on JSON format as Response

@router.post("/query_tips_in_json", tags=[Tags.predict_result])
async def query(level: str):
    messages_chat = []
    temparature = 0.5
    max_tokens = 500

    input_prompt = """You are a mental health specialist. Now I have built a function that upon analyzing a text will give a value between a range of 0 to 9 based on the person's mental health condition. Now the text will be analyzed based on three factors. Such as,

1. Mood of the text: The possible moods are joy, sadness, anger, and fear. Based on the text we can get one among the four values.
2. Stress level: Based on the text, we can get one of the two possible values: the person is in stress and the person is not in stress.
3. Suicidal level: Based on the text, we can get one of the two possible values: the text is suicidal or non-suicidal.

Now, the value between the range 0-9 can be decided by the above 3 factors via the following combinations. Such as,

1. If the mood of the text is joy then it will give the value 0 and the person's mental health level is excellent.
2. If the mood of the text is sadness, if the stress level of the text is the person is not in stress then the value is 1. 
3. If the mood of the text is anger, if the stress level of the text is the person is not in stress then the value is 2. 
4. If the mood of the text is fear, if the stress level of the text is the person is not in stress then the value is 3. 
5. If the mood of the text is sadness, if the stress level of the text is the person is in stress and the suicidal level of the text is non suicidal then the value is 4. 
6. If the mood of the text is anger, if the stress level of the text is the person is in stress and the suicidal level of the text is non suicidal then the value is 5. 
7. If the mood of the text is fear, if the stress level of the text is the person is in stress and the suicidal level of the text is non suicidal then the value is 6. 
8. If the mood of the text is sadness, if the stress level of the text is the person is in stress and the suicidal level of the text is suicidal then the value is 7. 
9. If the mood of the text is anger, if the stress level of the text is the person is stressed and the suicidal level of the text is suicidal then the value is 8. 
10. If the mood of the text is fear, if the stress level of the text is the person is in stress and the suicidal level of the text is suicidal then the value is 9. 

Now, based on the value you have to give some tips that have the potential to improve the person's mental health conditions. while giving the tips do not say something like "This person is in ..." or "Since the mood of the text indicates..." or " value ...:" Just give a positive sentence at the beginning and give the tips with points. The introductory sentence should be positive and encouraging.

Now the value is - f"{level}" """

    messages_chat.append({"role":"user","content":f"{input_prompt}"})
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages= messages_chat,
        temperature=temparature,
        max_tokens=max_tokens,
    )

    response = completion.choices[0].message.content

    # Extracting brief and tips
    brief, *tips = response.split("\n")

    # Removing the initial bullet point and formatting the tips
    tips = [tip.strip()[3:] for tip in tips if tip.strip()]

    # Constructing the JSON response
    json_response = {
        "brief": brief.strip(),
        "tips": tips
    }

    return json_response