# cfbStatsApi.py

import json
import warnings
import cfbStatsLib as api
from flask import Flask, jsonify, request, make_response

warnings.filterwarnings("ignore")

app = Flask(__name__)

# Endpoint definitions here


if __name__ == '__main__':
	app.run(port=8000)
