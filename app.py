from flask import Flask, render_template, url_for, redirect
from flask import request, jsonify
from flask_cors import CORS
#from dotenv import load_dotenv
import openai
import os



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category')
def category_page():
    return render_template('category.html')

@app.route('/category/korean')
def korean_page():
    return render_template('korean.html')

@app.route('/category/chinese')
def chinese_page():
    return render_template('chinese.html')

@app.route('/category/western')
def western_page():
    return render_template('western.html')

@app.route('/category/japanese')
def japanese_page():
    return render_template('japanese.html')


@app.route('/category/basket')
def basket_page():
    return render_template('basket.html')

dish = "제육볶음"
@app.route('/gpt', methods =['GET','POST'])
def chatGPT():
    # set api key
    #openai.api_key = os.environ.get("FLASK_API_KEY")
    openai.api_key = ""
    # Call the chat GPT API
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": "You are a competent cook who knows Korean, Chinese, Western, and Japanese"},
        {"role": "user", "content": f"${dish}의 재료와 요리 방법을 알려줘" }
        ],
    )
    result = completion.choices[0].message.content
    return render_template('gpt.html', result = result)

if __name__ == '__main__':
    app.run()
