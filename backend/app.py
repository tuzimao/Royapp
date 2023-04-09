import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='')
api = Api(app)
CORS(app, origins=["http://localhost:8080"])

# api key
openai.api_key = os.environ.get("OPENAI_API_KEY")


class GPTResponse(Resource):
    def get(self):

        user_question = request.args.get('prompt')
        system_role = request.args.get('systemRole')

        if not user_question:
            return jsonify({"error": "No prompt provided"})
        if not system_role:
            system_role = "Vancouver realestate advisor"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a {system_role}. What do you ask?"},
                {"role": "user", "content": user_question},
            ],
            max_tokens=350,
            n=1,
            stop=None,
            temperature=0.2,
        )
        response = response['choices'][0]['message']['content']

        return jsonify(gpt_response=response.strip())


class GPTRegenerateResponse(Resource):
    def get(self):

        user_question = request.args.get('prompt')
        system_role = request.args.get('systemRole')

        if not user_question:
            return jsonify({"error": "No prompt provided"})
        if not system_role:
            system_role = "Vancouver realestate advisor"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a {system_role}. What do you ask?"},
                {"role": "user", "content": user_question},
            ],
            max_tokens=350,
            n=1,
            stop=None,
            temperature=0.9,  # 使用稍微更高的 temperature 值以获得不同的回答
        )
        response = response['choices'][0]['message']['content']

        return jsonify(gpt_response=response.strip())


api.add_resource(GPTRegenerateResponse, '/api/regenerate-gpt-response')
api.add_resource(GPTResponse, '/api/gpt-response')


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
