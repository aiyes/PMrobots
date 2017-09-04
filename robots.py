from flask import Flask,request,jsonify
from APP.TBRobots import Robot
import json
import time
from APP.TBRobotCon import Method,is_ok


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/askpricesh',methods=['POST'])
def Ask_Price_SH():
    is_ok()
    try:
        data = request.get_data()
        j_data=json.loads(data.decode())
        print(j_data)
        MD=Method()
        info=MD.AskPrice_SH_MN(dic=j_data)
        return jsonify(info)
    except Exception as e:
        return jsonify({'flag': 500, 'infomation': e})



@app.route('/askpricewd',methods=['POST'])
def Ask_Price_WD():
    is_ok()
    try:
        data = request.get_data()
        j_data=json.loads(data.decode())
        MD=Method()
        info=MD.AskPrice_WD_MN(dic=j_data)
        return jsonify(info)
    except Exception as e:
        return jsonify({'flag':500,'infomation':e})

if __name__ == '__main__':
    app.run()
    #app.run(host='192.168.98.142')
