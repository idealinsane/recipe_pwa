from flask import Flask, render_template, request
import os, re
from dotenv import load_dotenv
import google.generativeai as genai

# Flask 앱 초기화
app = Flask(__name__)

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Google Gemini API 설정
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash') 

# 요리 리스트
cuisines = [
    "",
    "Italian",
    "Mexican",
    "Indian",
    "Chinese",
    "Japanese",
    "French",
    "Mediterranean",
    "American",
    "Thai",
    "Greek"
]
dietary_restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Carb",
    "Organic",
    "Locally Sourced",
]

languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Indonesian': 'id',
    'Thai': 'th',
    'Filipino': 'tl',
    'Vietnamese': 'vi',

}

@app.route('/')
def index():
    return render_template('index.html', cuisines=cuisines, dietary_restrictions=dietary_restrictions, 
                           languages=languages)

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # 사용자 입력 받기
    ingredients = request.form.getlist('ingredient')
    selected_cuisine = request.form.get('cuisine')
    selected_restriction = request.form.getlist('restrictions')
    selected_language = request.form.get('language')

    print('selected_cuisine: ' + selected_cuisine)
    print('selected_restrictions: ' + str(selected_restriction))
    print('selected_language: ' + selected_language)

    # 프롬프트 구성
    prompt = f"""Craft a recipe in HTML in {selected_language} using \
    {', '.join(ingredients)}. It's okay to use some other necessary \
    ingredients. Ensure the recipe ingredients appear at the top, \
    followed by the step-by-step instructions."""

    

    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."

    if selected_cuisine:
        prompt += f"The cuisine should be {selected_cuisine}."
    if selected_restriction and len(selected_restriction) > 0:
        prompt += f"The recipe should have the following restrictions: {','.join(selected_restriction)}."

    # Gemini API 호출
    try:
        response = model.generate_content(prompt)
        recipe = response.text  # Gemini 응답에서 텍스트 추출
        # ```html ... ``` 패턴 제거
        recipe = re.sub(r"```html\s*([\s\S]*?)```", r"\1", response.text).strip()
    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"


    return render_template(
    'recipe.html',  # 또는 index.html에 출력할 영역이 있다면 그대로
    recipe=recipe,
    cuisines=cuisines,
    dietary_restrictions=dietary_restrictions
)



if __name__ == '__main__':
    app.run(debug=True)
