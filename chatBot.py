import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='./root/.env')

app = Flask(__name__)

# Generate function to interact with Gemini API
def generate(user_input):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
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
                text="""Provide clear, compassionate advice and guidance for individuals who are either new victims of sextortion or currently being affected by it. Address the following:

What to do if you're a victim: Offer immediate steps for someone who has just discovered they are being targeted, such as how to protect themselves and their personal information.

Recognizing the signs of sextortion: Help users understand common tactics used by perpetrators to manipulate or coerce victims into complying with demands.

How to report and seek help: Advise on reporting the situation to authorities, online platforms, and family members or guardians. Mention any available hotlines or resources that can provide support.

Emotional support: Provide reassurance that victims are not alone and share healthy ways to deal with the emotional and psychological impact, such as reaching out to trusted friends or seeking professional help.

Prevention tips for the future: Offer advice on how to protect oneself from future sextortion attempts, including safeguarding personal information and recognizing red flags in online interactions.

Ensure the tone is empathetic, empowering, and supportive, focusing on providing hope and actionable steps for victims to take control of their situation. Write in normal text and try to be human like with it. Say regular sentences no "**" bolding

or italics and such. Try to keep it at a simpler and more minimum level too but still give appropriate amount of information"""
            ),
        ],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text

    return response_text

# Home route
@app.route('/')
def index():
    return render_template('chatBot.html')

# API route to handle the user input and return the response
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = generate(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
