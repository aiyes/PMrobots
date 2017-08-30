from flask import Flask,request,jsonify
import json

import time
from APP.TBRobotCon import Method

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/askpricesh',methods=['POST'])
def Ask_Price_SH():
    data = request.get_data()
    j_data=json.loads(data.decode())
    MD=Method()
    info=MD.AskPrice_SH_MN(dic=j_data)
    return jsonify(info)


if __name__ == '__main__':
    app.run(host='192.168.98.142')
