import os
import requests

from flask import Flask, request

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PROMPT = """I need you to generate a simple HTML page for the website "thesiteofeverything.com", a website that has every type of content in existence.
The page that you're going to generate is located at the path "/{path}", and was requested with the following query params: {params}.
Respond with nothing else but the HTML content of the page. You can include links to other pages. Try to be a bit funny if possible.
If you're unable to fullfil the request, generate a HTML page with an error message that is relevant to the context.
"""

def get_page(path, params):
    prompt = PROMPT.format(path=path, params=dict(params))
    resp = requests.post(
        url="https://api.openai.com/v1/chat/completions",
        headers={
            "authorization": f"Bearer {OPENAI_API_KEY}"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return get_page(path=path, params=request.args)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
