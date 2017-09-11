from flask import Flask,request,jsonify
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import json
import time
from APP.TBRobotCon import Method,is_ok

#monkey.patch_all()
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#app.config.update(DEBUG=True)


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
        return jsonify({'flag': 500, 'infomation': ''})


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
    #http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    #http_server.serve_forever()
