import time
import json
import websocket

url = "wss://autoglm-api.zhipuai.cn/openapi/v1/autoglm/developer"
headers = {
    "Authorization": "In-WelXg_A7jnMlbbdc7FqCvnbGGs3W1IyJAtrjDp0rRjvEXePhXuZ2sfEMq0yEpEgiNoYL46Ujpb-tySCS1Gg.UkggS2f2XzJvx_QbDyqURfEorcdLvTbTCom0h4iv2e0"  # 替换为实际 token
}


def on_message(ws, message):
    print("Received:", message)

    # 解析接收到的消息
    try:
        data = json.loads(message)

        if data["msg_type"] == "server_task":
            task_data = data["data"]["data_agent"]
            if task_data["action"] == "finish":
                print("✅ 任务完成！")
                print(f"🔍 {task_data['message']}")
                print(f"📌 会话ID: {task_data['session_id']}")
                print(f"📌 请求ID: {task_data['request_id']}")

        elif data["msg_type"] == "server_error":
            error_data = data["data"]
            print(f"❌ 错误: {error_data['message']}")

    except Exception as e:
        print(f"消息解析失败: {e}")


# 在 on_open 回调中添加重试逻辑
def on_open(ws):
    print("WebSocket connection opened.")

    # 添加延迟后重试
    time.sleep(1)

    # 获取用户实时输入
    user_input = input("请输入您的指令: ")

    send_data = {
        "timestamp": int(time.time()),
        "conversation_id": "",
        "msg_type": "client_test",
        "msg_id": "",
        "data": {
            "biz_type": "test_agent",
            "instruction": user_input
        }
    }

    # 将数据转换为 JSON 字符串并发送
    ws.send(json.dumps(send_data))


def on_error(ws, error):
    print("Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


# 创建 WebSocket 连接
ws = websocket.WebSocketApp(
    url,
    header=headers,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# 开始运行
ws.run_forever()