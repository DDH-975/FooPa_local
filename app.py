from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mainpage')
def main_page():
    return render_template('mainpage.html')

@app.route('/mainpage/korean')
def korean_page():
    return render_template('korean.html')

@app.route('/mainpage/chinese')
def chinese_page():
    return render_template('chinese.html')

@app.route('/mainpage/western')
def western_page():
    return render_template('western.html')

@app.route('/mainpage/japanese')
def japanese_page():
    return render_template('japanese.html')

@app.route('/mainpage/recipe')
def recipe_page():
    return render_template('recipe.html')

@app.route('/mainpage/basket')
def basket_page():
    return render_template('basket.html')


if __name__ == '__main__':
    app.run()
