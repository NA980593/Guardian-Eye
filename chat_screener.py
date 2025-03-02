import base64
import os
from google import genai
from google.genai import types

key = 'GEMINI_API_KEY'

def isMessageSuspicious(message):
    if "yes" in analyze_message(message):
        return True
    if "no" in analyze_message(message):
        return False

def analyze_message(message):
    client = genai.Client(
        # api_key=os.getenv(key),
        api_key="", # remove this before deploying
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=message
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(
                text="""you will receive a message. based off that message, if you detect any sort of phishing,
                scamming, or especially any sextortion flag it. if there is even the littlest amout at all flag it.
                if it has any at all and is flagged respond only with \"yes\" otherwise if it is a normal messsage
                respond with \"no\""""
            ),
        ],
    )

    response = client.models.generate_content(
    model=model,
    contents=contents, config=generate_content_config)
    return response.text

# print(isMessageSuspicious("Hi"))