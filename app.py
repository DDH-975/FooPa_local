from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def main_page():
    return render_template('mainpage.html')

@app.route('/')
def korean_page():
    return render_template('korean.html')

@app.route('/')
def chinese_page():
    return render_template('chinese.html')

@app.route('/')
def western_page():
    return render_template('western.html')

@app.route('/')
def japanese_page():
    return render_template('japanese.html')

@app.route('/')
def recipe_page():
    return render_template('recipe.html')

@app.route('/')
def basket_page():
    return render_template('basket.html')


if __name__ == '__main__':
    app.run()
