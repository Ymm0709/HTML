from myflask import myflask
import os

# 创建服务器实例，host="0.0.0.0" 表示局域网设备都能访问
app = myflask(host="0.0.0.0", port=8080)

# 根路径直接返回 HTML
@app.route("/", methods=["GET"])
def home():
    with open("Amorim.html", "r", encoding="utf-8") as f:
        return f.read()

# 文件名路径也可以访问
@app.route("/Amorim.html", methods=["GET"])
def page():
    with open("Amorim.html", "r", encoding="utf-8") as f:
        return f.read()

# 添加静态文件支持（图片、CSS等）
@app.route("/ruben_amorim.jpg", methods=["GET"])
def serve_image():
    return serve_static_file("ruben_amorim.jpg")

def get_content_type(filename):
    """根据文件扩展名返回Content-Type"""
    ext = filename.lower().split('.')[-1]
    content_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'css': 'text/css',
        'js': 'application/javascript',
        'html': 'text/html',
        'txt': 'text/plain'
    }
    return content_types.get(ext, 'application/octet-stream')

def serve_static_file(filename):
    """处理静态文件请求，只使用Python标准库"""
    if not os.path.exists(filename):
        return f"<h1>404 Not Found</h1><p>File {filename} not found</p>", "404 Not Found"
    
    # 获取文件类型
    content_type = get_content_type(filename)
    
    # 读取文件内容
    with open(filename, "rb") as f:
        content = f.read()
    
    # 返回 (content, status, content_type) 元组
    return content, "200 OK", content_type

# 在 run 方法里加打印信息，方便调试
def run_with_log(self):
    import socket
    with socket.socket() as s:
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"服务器启动在 {self.host}:{self.port}")
        print("等待连接...")
        while True:
            conn, addr = s.accept()
            with conn:
                print("连接地址：", addr)
                request = conn.recv(4096).decode("utf-8", errors="ignore")
                print("收到请求:\n", request.split("\r\n")[0])  # 打印请求行
                response = self._handle_request(request)
                conn.sendall(response.encode("utf-8"))

# 替换原来的 run 方法
app.run = lambda: run_with_log(app)

# 启动服务器
app.run()
