import os
import re
import requests


class ReadmeUpdater:
    def __init__(self, file_path):
        self.file_path = file_path

    def check_url_availability(self, url, timeout=5):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return True, "网址可以正常访问"
            else:
                return False, f"网址访问出错，状态码为 {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "网址访问超时"
        except requests.exceptions.RequestException as e:
            return False, f"网址访问出现异常：{str(e)}"

    def replace_status_with_error(self, match):
        status = match.group(1)
        if "⭐Running" in status:
            return '<span style="color: red">❌Error</span>'
        else:
            return status

    def update_readme(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            content = file.read()

        pattern = r"\[.*?\]\((.*?)\)"
        matches = re.findall(pattern, content)

        new_content = content
        for url in matches:
            result, message = self.check_url_availability(url)
            print(url, message)
            if not result:
                new_content = re.sub(
                    f'({re.escape(url)}.*?)<span style="color: green">⭐Running</span>',
                    self.replace_status_with_error,
                    new_content,
                )

        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(new_content)


if __name__ == "__main__":
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(current_dir, "README.md")

    # 创建 ReadmeUpdater 实例并调用 update_readme 方法
    updater = ReadmeUpdater(readme_path)
    updater.update_readme()
