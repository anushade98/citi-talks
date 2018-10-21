from flask import Flask, request, render_template, jsonify
from shopping_mode import run_shopping_mode
from account_mode import run_account_mode

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('./index.html')


@app.route('/api/query', methods=['POST'])
def query():
    json_input = request.get_json()
    print(json_input)
    audio = json_input['audioRaw']
    open('audio.mp3', 'wb+').write(audio)
    result_shopping = run_shopping_mode()
    result_account = run_account_mode()

    answer = result_account + result_shopping
    print(jsonify({"responses":answer}))
    return(jsonify({"responses":answer}))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8080)
