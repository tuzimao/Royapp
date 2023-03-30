import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
CORS(app)

# api key
openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


class GPTResponse(Resource):
    def get(self):

        user_question = request.args.get('prompt')
        if not user_question:
            return jsonify({"error": "No prompt provided"})

        response = openai.Completion.create(
            engine="davinci",
            prompt=user_question,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            n=1,
            stop=None,
        )
        return jsonify(gpt_response=response.choices[0].text.strip())


api.add_resource(GPTResponse, '/api/gpt-response')

if __name__ == '__main__':
    app.run(debug=True)
