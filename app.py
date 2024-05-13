from flask import Flask, render_template, url_for, redirect, session
from flask import request, jsonify
#from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import xmltodict
import json
import requests
from flask import Flask, render_template, request, jsonify, make_response
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity, jwt_required,
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies, create_refresh_token,

)
from config import CLIENT_ID, REDIRECT_URI
from controller import Oauth
from model import UserData, UserModel


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "123"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 30
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 100
jwt = JWTManager(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/oauth")
def oauth_api():
    """
    # OAuth API [GET]
    사용자로부터 authorization code를 인자로 받은 후,
    아래의 과정 수행함
    1. 전달받은 authorization code를 통해서
        access_token, refresh_token을 발급.
    2. access_token을 이용해서, Kakao에서 사용자 식별 정보 획득
    3. 해당 식별 정보를 서비스 DB에 저장 (회원가입)
    3-1. 만약 이미 있을 경우, (3) 과정 스킵
    4. 사용자 식별 id를 바탕으로 서비스 전용 access_token 생성
    """
    code = str(request.args.get('code'))

    oauth = Oauth()
    auth_info = oauth.auth(code)
    user = oauth.userinfo("Bearer " + auth_info['access_token'])

    user = UserData(user)
    UserModel().upsert_user(user)

    resp = make_response(render_template('index.html'))
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    resp.set_cookie("logined", "true")
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp

@app.route('/token/refresh')
@jwt_required(refresh=True)
def token_refresh_api():
    """
    Refresh Token을 이용한 Access Token 재발급
    """
    user_id = get_jwt_identity()
    resp = jsonify({'result': True})
    access_token = create_access_token(identity=user_id)
    set_access_cookies(resp, access_token)
    return resp


@app.route('/token/remove')
def token_remove_api():
    """
    Cookie에 등록된 Token 제거
    """
    resp = jsonify({'result': True})
    unset_jwt_cookies(resp)
    resp.delete_cookie('logined')
    return resp

@app.route('/oauth/url')
def oauth_url_api():
    """
    Kakao OAuth URL 가져오기
    """
    return jsonify(
        kakao_oauth_url="https://kauth.kakao.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code" \
        % (CLIENT_ID, REDIRECT_URI)
    )

@app.route("/userinfo")
@jwt_required()
def userinfo():
    """
    Access Token을 이용한 DB에 저장된 사용자 정보 가져오기
    """
    user_id = get_jwt_identity()
    userinfo = UserModel().get_user(user_id).serialize()
    return jsonify(userinfo)



@app.route("/oauth/refresh", methods=['POST'])
def oauth_refesh_api():
    """
    # OAuth Refresh API
    refresh token을 인자로 받은 후,
    kakao에서 access_token 및 refresh_token을 재발급.
    (% refresh token의 경우,
    유효기간이 1달 이상일 경우 결과에서 제외됨)
    """
    refresh_token = request.get_json()['refresh_token']
    result = Oauth().refresh(refresh_token)
    return jsonify(result)

@app.route("/oauth/userinfo", methods=['POST'])
def oauth_userinfo_api():
    """
    # OAuth Userinfo API
    kakao access token을 인자로 받은 후,
    kakao에서 해당 유저의 실제 Userinfo를 가져옴
    """
    access_token = request.get_json()['access_token']
    result = Oauth().userinfo("Bearer " + access_token)
    return jsonify(result)



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




# API로부터 레시피 데이터 가져오기
def get_recipes():
    key = "fc0d6fc8e41441019501"
    url = f"http://openapi.foodsafetykorea.go.kr/api/{key}/COOKRCP01/xml/1/999"
    response = requests.get(url)
    content = response.content

    data_dict = xmltodict.parse(content)

    recipes = data_dict['COOKRCP01']['row']
    return recipes

# 데이터 필터링
def filter_recipes(category):
    recipes = get_recipes()
    filtered_recipes = []

    for recipe in recipes:
        if 'RCP_PAT2' in recipe and category in recipe['RCP_PAT2']:
            filtered_recipes.append(recipe)
    return filtered_recipes


#카테고리 페이지
@app.route('/category')
def category():
    return render_template('category.html')

@app.route('/address')
def address():
    return render_template('address.html')





# 밥 카테고리
@app.route('/rice')
def rice():
    recipes = filter_recipes('밥')
    return render_template('recipes.html', recipes=recipes)


# 반찬 카테고리
@app.route('/side_dish')
def side_dish():
    recipes = filter_recipes('반찬')
    return render_template('recipes.html', recipes=recipes)


# 국&찌개 카테고리
@app.route('/soup')
def soup():
    recipes = filter_recipes('국&찌개')
    return render_template('recipes.html', recipes=recipes)


# 후식 카테고리
@app.route('/dessert')
def dessert():
    recipes = filter_recipes('후식')
    return render_template('recipes.html', recipes=recipes)


# 일품 요리 카테고리
@app.route('/high_end_food')
def high_end_food():
    recipes = filter_recipes('일품')
    return render_template('recipes.html', recipes=recipes)


# 레시피 상세정보
@app.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipes = get_recipes()
    for recipe in recipes:
        if int(recipe['@id']) == recipe_id:
            return render_template('recipe_detail.html', recipe=recipe)
    return "Recipe not found."


#을식 검색
@app.route('/search')
def search():
    query = request.args.get('query')
    filtered_recipes = filter_recipes_by_query(query)
    return render_template('recipes.html', recipes=filtered_recipes)
def filter_recipes_by_query(query):
    recipes = get_recipes()
    filtered_recipes = [recipe for recipe in recipes if query.lower() in recipe['RCP_NM'].lower()]
    return filtered_recipes


#장바구니 페이지 (재료 파싱)
@app.route('/basket/<int:recipe_id>')
def basket(recipe_id):
    recipes = get_recipes()
    for recipe in recipes:
        if int(recipe['@id']) == recipe_id:
            if 'RCP_PARTS_DTLS' in recipe:
                ingredients = recipe['RCP_PARTS_DTLS'].split(',')  # 쉼표로 재료 구분
                ingredients = [ingredient.strip() for ingredient in ingredients]  # 공백 제거
                return render_template('basket.html', ingredients=ingredients)
            else:
                return "Ingredients not found."
    return "Recipe not found."


@app.route('/send-ingredients', methods=['POST'])
def send_ingredients():
    selected_ingredients = request.form.getlist('ingredients')

    data = {'ingredients': selected_ingredients}
    shopper_app_url = 'http://127.0.0.1:5001/receive-ingredients'

    response = requests.post(shopper_app_url, json=data)

    if response.status_code == 200:
        return "재료를 쇼퍼 앱으로 성공적으로 전송했습니다."
    else:
        return '재료 전송에 실패했습니다.', 500


if __name__ == '__main__':
    app.run(debug=True)
