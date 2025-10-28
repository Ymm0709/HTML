from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

# 用字典管理其他人的 HTML 文件
others_html = {
    "A": "A.html",
    "B": "B.html",
    "C": "C.html"
}

# 根路径显示你的 HTML，并附带其他链接
@app.route("/")
def home():
    # 生成按钮
    buttons_html = "".join([
        f'<a href="/view/{key}" class="btn">{key}</a>' for key in others_html
    ])
    
    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>我的简历</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                text-align: center;
                background-color: #f9f9f9;
            }}
            h1 {{
                margin-bottom: 20px;
            }}
            iframe {{
                width: 80%;
                height: 500px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }}
            .buttons {{
                margin-top: 30px;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                margin: 0 10px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                transition: background-color 0.3s;
            }}
            .btn:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <h1>我的简历</h1>
        <iframe src="/my"></iframe>

        <div class="buttons">
            <h2>查看其他人的简历</h2>
            {buttons_html}
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

# 显示你的 HTML
@app.route("/my")
def my_html():
    return send_from_directory('.', 'Amorim.html')

# 查看别人 HTML
@app.route("/view/<key>")
def view_html(key):
    filename = others_html.get(key)
    if filename:
        return send_from_directory('.', filename)
    return "不存在该页面", 404

# 使用 Flask 的 /static 提供静态资源，无需自定义图片路由

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
