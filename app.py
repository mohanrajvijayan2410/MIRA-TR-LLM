from flask import Flask, render_template, request, jsonify
import groq

app = Flask(__name__)

# Initialize the Groq client with your API key
try:
    client = groq.Groq(api_key="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")
except Exception as e:
    print(f"Error initializing Groq client: {e}")

import requests
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    groq_reply = ask_ai(user_message)
    ls = groq_reply.split('\n')
    print(ls)
    groq_reply = '<br>'.join(ls)
    return jsonify({'reply': groq_reply})

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
             messages=[
                {"role": "system", "content": """You are an AI agent.
Do not genrate additional instructions, make the instructions less in number
You should stricly folllow this output template


this is the Output template:
Task: Prepare Five Bread Sandwiches with Cheese
Sequence of Instructions:
1. Instruction 1: Take 10 slices of White bread.
• Type: SIMPLE INSTRUCTION
   Duration: 1 minute
2. Instruction 2: Add cheese to 10 slices of White bread.
• Type: INSTRUCTION WITH PURPOSE
   Duration: 1 minute
3. Instruction 3: Optionally, heat the sandwiches using a Sandwich maker or Grill.
Type: EXCLUSIVE INSTRUCTION
    Duration: 3 minutes (optional)
4. Instruction 4: Pickup the sandwiches then serve them.
• Type: INSTRUCTION WITH SEQUENCE
    Duration: 30 seconds
Total Time Calculation:
• Without Heating: 2 minutes 30 seconds
• With Heating: 5 minutes 30 seconds
This sequence includes all the necessary instructions for preparing and serving the sandwiches,
using the appropriate instruction types as per the MIRA protocol.

Important
You have to generate one action for each instruction : TYPE: SIMPLE INSTRUCTION
 • Instructions can include one object or multiple objects (e.g. take pen or take
 pens and papers) TYPE: SIMPLE INSTRUCTIONS
 • Each instruction can include a goal- here the instruction should have the
 intention of goal perspective (e.g, take pen if you have the intention of writing,
 take pen if you want to write) TYPE: INSTRUCTION WITH PURPOSE
 • Each instruction can include multiple objects which are exclusive (e.g. take pen
 or pencil)- Instructions: TYPE: EXCLUSIVE INSTRUCTION
 • If there are options between actions, include or within that instructions, to
 represent exclusive or (e.g. Go by walk or take a car to reach destination)
 TYPE: EXCLUSIVE INSTRUCTION
 • If two actions are provided in a sequence, use “then” and do not use “and” (e.g. Take pen then write) TYPE: INSTRUCTION WITH SEQUENCE
                 """},
                {"role": "user", "content": prompt},
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            stream=False,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during API call: {e}")
        return "Sorry, there was an error processing your request."

def chat_ai(prompt):
    try:
        response = client.chat.completions.create(
             messages=[
                {"role": "system", "content": "You are chatbot give short chat responses"},
                {"role": "user", "content": prompt},
            ],
            model="mixtral-8x7b-32768",
            temperature=0.2,
            max_tokens=500,
            top_p=1.0,
            stream=False,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during API call: {e}")
        return "Sorry, there was an error processing your request."


@app.route('/', methods=['GET', 'POST'])
def index():
    gpt_response = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        gpt_response = ask_ai(user_input)
        print(gpt_response)
    return render_template('index.html', gpt_response=gpt_response)

if __name__ == "__main__":
    app.run(debug=True)
