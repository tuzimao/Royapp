import os

api_key = os.environ.get("OPENAI_API_KEY")

if api_key:
    print("OPENAI_API_KEY is set.")
    print(f"API Key: {api_key}")  # 这将输出您的 API 密钥，请确保不要在任何地方泄漏它
else:
    print("OPENAI_API_KEY is not set.")
