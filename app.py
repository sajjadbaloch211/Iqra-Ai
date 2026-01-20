
from flask import Flask, render_template, request, jsonify
from chatbot import ChatBot

app = Flask(__name__)
bot = ChatBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = bot.get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
