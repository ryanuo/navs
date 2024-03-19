import re
import requests

# 读取 readme.md 文件
with open("readme.md", "r", encoding="utf-8") as file:
    content = file.read()


# 检查并更新链接状态
def check_link_status(match):
    name = match.group(1)
    link = match.group(2)

    try:
        response = requests.get(link)
        if response.status_code == 200:
            return f'| [{name}]({link}) | <span style="color: green">⭐Running</span> |'
        else:
            return f'| [{name}]({link}) | <span style="color: red">❌Error</span> |'
    except requests.exceptions.RequestException:
        return f'| [{name}]({link}) | <span style="color: red">❌Error</span> |'


updated_content = re.sub(
    r'\| \[([^\]]+)\]\(([^)]+)\) \| <span style="color: [a-zA-Z]+">.*?<\/span>',
    check_link_status,
    content,
)

# 将更新后的内容写入文件
with open("README.md", "w", encoding="utf-8") as file:
    file.write(updated_content)

print("File updated successfully")
