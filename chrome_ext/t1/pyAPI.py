from flask import Flask, request, jsonify
from flask_cors import CORS # 导入 CORS

app = Flask(__name__)
CORS(app) # 启用所有路由的 CORS

@app.route('/api/data', methods=['POST'])
def receive_data():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    print("---------------------------------")
    print("接收到来自 Chrome 扩展程序的数据：")
    print(f"标题 (title): {data.get('title')}")
    print(f"下载信息 (downloadInfo): {data.get('downloadInfo')}")
    print("---------------------------------")

    return jsonify({"message": "Data received successfully!", "data": data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)