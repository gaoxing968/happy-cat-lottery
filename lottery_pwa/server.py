"""
PWA 版彩票模拟开奖器 - 纯前端无后端
直接打开 index.html 即可使用，或用本服务器：
python server.py
访问: http://localhost:5002
"""

import http.server, socketserver, os, json

PORT = 5002
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Service-Worker-Allowed', '/')
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

print(f"🎰 PWA版启动中...")
print(f"   直接双击 index.html 打开也行")
print(f"   或浏览器访问: http://localhost:{PORT}")
print(f"   手机访问（同一WiFi）: http://电脑IP:{PORT}")
print(f"   Ctrl+C 停止")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()