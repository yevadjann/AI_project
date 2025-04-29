# logical, mature, optimistic, smart, win several sport events in football, my grades are 5 only
# AIzaSyCnsXkrkL1y1EXTH7NA20vUxv7ZFLEheYI
# gemini key

from flask import Flask, render_template, request, jsonify
import requests
import json
import google.generativeai as genai
import os
import re

app = Flask(__name__, static_folder='static', template_folder='templates')

genai.configure(api_key="AIzaSyCnsXkrkL1y1EXTH7NA20vUxv7ZFLEheYI") 
model = genai.GenerativeModel("gemini-1.5-pro-latest") 

generated_letters = {}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message', '')
    session_id = request.json.get('session_id', 'default')

    if not user_input.strip():
        return jsonify({'response': "Please enter something to get a response."})
    
    try:
        
        prompt = f"""Write a motivation letter for a university application. 
                    The student has the following qualities: {user_input}.
                    The letter should explain why they are applying to the university, highlight their achievements, strengths, and personal characteristics, and express their enthusiasm for studying at the institution.
                    Ensure the letter is formal, structured, and persuasive.
                    """

        # Start chat session
        chat = model.start_chat()

        # Send message to the chat
        response = chat.send_message(prompt)

        full_response = response.text

        generated_letters[session_id] = full_response

        return jsonify({
            'response': full_response,
            'ask_feedback': True
        })
        

    except Exception as e:
        import traceback
        print("Gemini Error:", e)
        traceback.print_exc()
        return jsonify({'response': f"Error generating letter: {str(e)}"})

@app.route('/revise_letter', methods=['POST'])
def revise_letter():
    session_id = request.json.get('session_id', 'default')
    feedback = request.json.get('feedback', '')
    existing_letter = generated_letters.get(session_id, '')
    
    if not existing_letter:
        return jsonify({'response': 'No original letter found to revise.'})
    

    revision_prompt = f"""
                        You are a text editor assistant. You will receive:
                        - A letter
                        - One specific user instruction

                        RULES:
                        - Only apply the exact instruction.
                        - Never rewrite or regenerate the whole letter.
                        - Do NOT make edits that were not mentioned.
                        - Keep everything else 100% unchanged.

                        ---
                        Instruction:
                        {feedback}

                        ---
                        Letter:
                        \"\"\"{existing_letter}\"\"\"

                        ---
                        Return ONLY the updated letter.
                        """
    
    try:
        # start chat session
        chat = model.start_chat(history=[
            {
                "role": "system",
                "parts": [
                    "You are a precise assistant that only edits specific words or lines based on user instruction. Never rewrite unless explicitly told to."
                ]
            }
        ]) 

        response = chat.send_message(revision_prompt)
        updated_letter = response.text

        generated_letters[session_id] = updated_letter

        return jsonify({'response': updated_letter})

    except Exception as e:
        print("Revision Error:", e)
        return jsonify({'response': "Error revising the letter."})
    
@app.route('/welcome_page')
def welcome_page():
    return render_template('welcome_page.html')


if __name__ == '__main__':
    app.run(debug=True)