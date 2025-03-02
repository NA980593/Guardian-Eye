from flask import Flask, render_template, request, jsonify
import os
from google import genai
from google.genai import types

# Initialize Flask app
app = Flask(__name__)

# Function to generate advice for sextortion
def generate_advice(input_text):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=input_text)],
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

Ensure the tone is empathetic, empowering, and supportive, focusing on providing hope and actionable steps for victims to take control of their situation."""
            ),
        ],
    )

    # Get the response using the Gemini API
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        return chunk.text


# Flask route to handle chat
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        model_response = generate_advice(user_input)
        return jsonify({"response": model_response})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
