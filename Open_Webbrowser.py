import webbrowser

# new = 0: mở trang trong cùng 1 page nếu có thể
# new = 1: mở một cửa sổ trình duyệt mới nếu có thể
# new = 2: mở một tab mới.

class open_webbrowser():
    def run_web(self, url):
        webbrowser.open(url, new=2)
