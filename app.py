from flask import Flask, render_template, request, jsonify
from openai_assistant import create_assistant, create_thread, add_message, run_thread

app = Flask(__name__)

assistant_id = create_assistant()
thread_id = create_thread()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    add_message(thread_id, user_message)
    response = run_thread(thread_id, assistant_id)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
