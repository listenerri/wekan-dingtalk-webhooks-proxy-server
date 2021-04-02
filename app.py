import json
from flask import Flask, escape, request, abort, Response

# TODO(ri): config.json reload

app = Flask(__name__)
app.debug = 1

@app.route('/api/wekan/webhook/', methods=["POST"])
def wekan_webhook():
    print("accepted a webhook")
    for k, v in request.json.items():
        print(k, v)
    return ("done")

if __name__ == '__main__':
    app.run()
