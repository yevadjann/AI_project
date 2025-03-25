from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyANKBGfWMBOIltrQ8jSF6CQ0x-A8wGv2rU"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={AIzaSyANKBGfWMBOIltrQ8jSF6CQ0x-A8wGv2rU}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message', '')

    if not user_input.strip():
        return jsonify({'response': "Please enter something to get a response."})
    
    try:
        prompt = f"Write a motivational letter for a student who has the following qualities: {user_input}. The letter should inspire confidence, highlight their strengths, and encourage them to continue their academic or professional journey."
        
        response = requests.post(
            GEMINI_API_URL,
            json={
                "prompt": prompt,  # Using the structured prompt to guide the model
                "temperature": 0.7,  # Adjust creativity of the response
                "max_output_tokens": 300
            }
        )

        
        print(response.status_code)  # Check the response status code
        print(response.text)

        if response.status_code == 200:
            ai_response = response.json().get("output", "No response from Gemini.")
        else:
            ai_response = "An error occurred while generating the response. Please try again later."

    except Exception as e:
        print("Google Gemini API Error:", e)
        ai_response = "An error occurred while generating the response. Please try again later."

    return jsonify({'response': ai_response})



if __name__ == '__main__':
    app.run(debug=True)