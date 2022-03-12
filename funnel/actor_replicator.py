import csv
import json
from .insta.client_fs import InstaPostManager
from .wp.client_http import WordpressPostManager

post_repo_path = "path/to/instaposts"
wp_config_file = json.load(open("../../settings/wp_config.json"))
insta_wp_map = {k: v for k, v in csv.reader(open("../../settings/insta_wp_map.csv"))}


if __name__ == "__main__":
    pm = InstaPostManager(post_repo_path)
    wpm = WordpressPostManager(wp_config_file, "https", status="live")

    for user, sub in insta_wp_map.items():
        struct_posts = pm.get_posts(user)
        all_tags = wpm.update_tags(sub, struct_posts)
        wpm.update_posts(sub, struct_posts, all_tags)
