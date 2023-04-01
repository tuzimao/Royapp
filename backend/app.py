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
        if not user_question:
            return jsonify({"error": "No prompt provided"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an Vancouver realestate advisor. You are helping a client find a home in Vancouver. What do you ask?"},
                {"role": "user", "content": user_question},
            ],
            max_tokens=350,
            n=1,
            stop=None,
            temperature=0.9,
        )
        response = response['choices'][0]['message']['content']

        return jsonify(gpt_response=response.strip())


api.add_resource(GPTResponse, '/api/gpt-response')


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
