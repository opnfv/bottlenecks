from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
import time
import json
from random import randint
import os
import yaml

app = Flask(__name__)
CORS(app)
@app.route("/greet")
def greet():
  return "hello"

@app.route("/answer", methods=["POST"])
def answer():
  app.logger.debug(request.form)
  app.logger.debug(request.data)
  if jsonify(request.form) != {} and 'ping' in request.form:
    return "answer: ping is: \"" + request.form['ping'] + "\" end."
  elif request.data != "":
        requestDict = json.loads(request.data)
        if 'ping' in requestDict:
                return "answer: the ping is: \"" + requestDict['ping'] + "\" end."
  else:
    return "answer ping is null"

@app.route("/answer2", methods=["POST"])
def answer2():
  # dataDict = json.loads(request.data)
  return "ok"

@app.route("/five")
def sleepFiveSeconds():
  time.sleep(5)
  return "five: receive the request."

@app.route("/ten")
def sleepTenSeconds():
  time.sleep(10)
  return "ten: receive the request."

@app.route("/switch")
def switchValue():
  value = randint(0, 10)
  if value > 4:
    return jsonify({'code':200, 'result': 'A'})
  else:
    return jsonify({'code':200, 'result': 'B'})

@app.route("/switch_2")
def switchValue_2():
  value = randint(0, 10)
  if value > 4:
    return jsonify({'code':200, 'result': 'C'})
  else:
    return jsonify({'code':200, 'result': 'D'})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5312, debug=True)