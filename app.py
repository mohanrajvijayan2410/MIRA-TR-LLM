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
    groq_reply = chat_ai(user_message)
    ls = groq_reply.split('\n')
    print(ls)
    groq_reply = '<br>'.join(ls)
    return jsonify({'reply': groq_reply})



def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
             messages=[
                {"role": "system", "content": """You are an AI agent. I’ll give you a list of available Objects (OBJ) and valid actions. Pick out correct objects from the list of Available objects. Duration of the task is also given. With these, you have to generate a sequence of instructions for the given task description. Compute the total time for all the number of tasks.
You should stricly folllow this output example
Output Example:
Available Objects:
Book 1
Book 2
Book 3
Book 4
Book 5
Task Sequence:
Take OBJ: Take Book 1 (0 minutes)
Read OBJ: Read the first chapter of Book 1 (5 minutes)
Bookmark OBJ: Bookmark the first chapter of Book 1 (0 minutes)
Take OBJ: Take Book 2 (0 minutes)
Read OBJ: Read the first chapter of Book 2 (5 minutes)
Bookmark OBJ: Bookmark the first chapter of Book 2 (0 minutes)
Take OBJ: Take Book 3 (0 minutes)
Read OBJ: Read the first chapter of Book 3 (5 minutes)
Bookmark OBJ: Bookmark the first chapter of Book 3 (0 minutes)
Take OBJ: Take Book 4 (0 minutes)
Read OBJ: Read the first chapter of Book 4 (5 minutes)
Bookmark OBJ: Bookmark the first chapter of Book 4 (0 minutes)
Take OBJ: Take Book 5 (0 minutes)
Read OBJ: Read the first chapter of Book 5 (5 minutes)
Bookmark OBJ: Bookmark the first chapter of Book 5 (0 minutes)
Repeat OBJ: Repeat steps TASK 1 to TASK 3 for all 5 books (25 minutes)
Arrange OBJ: Arrange all the books on the shelf (5 minutes)
Total Time Calculation:
Each read and bookmark task takes 5 minutes.
For five books: 5 minutes × 5 books = 25 minutes
Repeat step:25  minutes.
Arranging books on the shelf:  5 minutes
Total Time: 25 + 25 + 5 = 55 minutes.
                 """},
                {"role": "user", "content": prompt},
            ],
            model="mixtral-8x7b-32768",
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
            temperature=0.7,
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