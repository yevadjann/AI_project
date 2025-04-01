# ollama run deepseek-llm

from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__, static_folder='static', template_folder='templates')

DEEPSEEK_API_URL = "http://localhost:11434/api/generate"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message', '')

    if not user_input.strip():
        return jsonify({'response': "Please enter something to get a response."})
    
    try:
        
        prompt = f"""Write a motivation letter for a university application. 
                    The student has the following qualities: {user_input}.
                    The letter should explain why they are applying to the university, highlight their achievements, strengths, and personal characteristics, and express their enthusiasm for studying at the institution.
                    Ensure the letter is formal, structured, and persuasive.
                    """

        response = requests.post(
            DEEPSEEK_API_URL,
            json={
                "model": "deepseek-llm",  # Use the best available model
                "prompt": prompt,
                "temperature": 0.7,
                "max_tokens": 300
            },
            stream=True
        )

        print(response.status_code)  # Check the response status code
        print(response.text)

        if response.status_code == 200:
            full_response = ""

            for line in response.iter_lines():
                if line:  # Avoid empty lines
                    try:
                        data = json.loads(line.decode("utf-8"))  # Decode each line as JSON
                        full_response += data.get("response", "")  # Collect response text
                    except json.JSONDecodeError as e:
                        print("JSON Parsing Error:", e)
                        full_response = "An error occurred while processing the response."
                        break  # Stop processing on JSON error
            
            ai_response = full_response if full_response else "No response from DeepSeek."

        else:
            ai_response = "An error occurred while generating the response. Please try again later."
        
        

    except Exception as e:
        print("DeepSeek API Error:", e)
        ai_response = "An error occurred while generating the response. Please try again later."

    return jsonify({'response': ai_response})



if __name__ == '__main__':
    app.run(debug=True)