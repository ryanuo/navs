import os
import re
import requests
import yaml
import datetime


def check_url_availability(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True, "🌟"
        else:
            return False, "❌"
    except requests.exceptions.Timeout:
        return False, "❌"
    except requests.exceptions.RequestException:
        return False, "❌"


def get_badge_content(total_links, running, error):
    current_date = datetime.datetime.now().strftime("%Y/%m/%d")
    badge_content = "\n".join(
        [
            f"<!-- @badge-start -->",
            f"![](https://img.shields.io/badge/check_link-{current_date}-blue?style=flat-square)",
            f"![](https://img.shields.io/badge/link_totals-{total_links}-7C33FF?style=flat-square)",
            f"![](https://img.shields.io/badge/running-{running}-green?style=flat-square)",
            f"![](https://img.shields.io/badge/error-{error}-FF3336?style=flat-square)",
            f"<!-- @badge-end -->",
        ]
    )
    return badge_content


class ReadmeUpdater:
    def __init__(self, file_path, link_file_path):
        self.file_path = file_path
        self.link_file_path = link_file_path

    def update_readme(self):
        with open(self.link_file_path, "r", encoding="utf-8") as file:
            links = yaml.load(file, Loader=yaml.SafeLoader)

        total_links = len(links)
        running = sum(1 for item in links if check_url_availability(item["link"])[0])
        error = total_links - running
        # Generate badge content
        badge_content = get_badge_content(total_links, running, error)

        readme_content = "<!-- @start -->\n"
        readme_content += "| title | link | status |\n"
        readme_content += "| ----- | ---- | :----: |\n"
        for item in links:
            title = item["title"]
            link = item["link"]
            result, status_icon = check_url_availability(link)
            print(f"「{title}」{link}：{status_icon}")
            readme_content += f"| {title} | <a href='{link}' target='_blank'>{link}</a> | {status_icon} |\n"
        readme_content += "<!-- @end -->"

        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                original_content = file.read()

            # Replace badge content
            badge_pattern = rf"(<!-- @badge-start -->).*?(<!-- @badge-end -->)"
            new_content = re.sub(
                badge_pattern, badge_content, original_content, flags=re.DOTALL
            )

            # Replace table content
            table_pattern = rf"(<!-- @start -->).*?(<!-- @end -->)"
            new_content = re.sub(
                table_pattern, readme_content, new_content, flags=re.DOTALL
            )

            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(new_content)
        else:
            # README.md does not exist, create it
            new_content = badge_content + "\n" + readme_content
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(new_content)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(current_dir, "README.md")
    link_path = os.path.join(current_dir, "link.yaml")
    updater = ReadmeUpdater(readme_path, link_path)
    updater.update_readme()
