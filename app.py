from flask import Flask, render_template

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

@app.route('/category/gpt')
def gpt_page():
    return render_template('gpt.html')

@app.route('/category/basket')
def basket_page():
    return render_template('basket.html')


if __name__ == '__main__':
    app.run()
