import re
import requests
import logging
from requests.auth import HTTPBasicAuth
from time import sleep
from datetime import datetime


class WordpressPostManager:

    tags_api = f"index.php?rest_route=/wp/v2/tags"
    post_api = f"index.php?rest_route=/wp/v2/posts"
    logger = logging.getLogger("WPM")

    def __init__(self, config, protocol="https", status="live"):

        self.config = config
        self.status = status
        self.protocol = re.sub("[^https]","",protocol)

    def update_tags(self, subdomain, posts):
        #Actualizar Tags bajándolos todos primero y solo posteando los que faltan
        cfg = self.config[subdomain]
        api_url = f"{self.protocol}://{subdomain}.{cfg['wp_domain']}/{self.tags_api}"
        auth_obj = HTTPBasicAuth(cfg["wp_user"], cfg["wp_pwd"])
        tags = {}
        for pp in posts:
            self.logger.debug(f"Tags for: {pp.title}")
            for tagcased in pp.hashtags:
                tag = tagcased.lower()
                if tag not in tags:
                    self.logger.debug(f"Checking {tag} in {api_url}")
                    if self.status == "live":
                        response = requests.post(api_url, auth=auth_obj, json={"name":tag[1:]})
                        if response.status_code == 201:
                            self.logger.debug(f"Tag created: {tag}")
                            tags[tag] = response.json()["id"]
                        else:
                            tags[tag] = response.json()["data"]["term_id"]
                            self.logger.debug(f"Tag existed: {tag}->{tags[tag]}")
                        sleep(0.2)
        return tags

    # Layout de la pagina de Wordpress basada en el post
    def build_page(self, subdomain, post, all_tags):
        cfg = self.config[subdomain]
        total_jpgs = len(post.jpgs)
        wp_tpl = f"""<!-- wp:gallery {{"linkTo":"none"}} -->
        <figure class="wp-block-gallery has-nested-images columns-default is-cropped columns-{min(3,total_jpgs)}">"""
        for jpg in post.jpgs:
            wp_tpl += f"""
            <!-- wp:image {{"sizeSlug":"large"}} -->
            <figure class="wp-block-image size-large">
            <img src="/wp-content/uploads/{cfg['img_path']}/{jpg}"/>
            </figure>
            <!-- /wp:image -->"""
        wp_tpl += f"""<figcaption class="blocks-gallery-caption">{post.description}</figcaption></figure>"""
        for mp4 in post.mp4s:
            wp_tpl += f"""
            <!-- wp:video -->
            <figure class="wp-block-video">
            <video controls src="/wp-content/uploads/{cfg['img_path']}/{mp4}"></video>
            </figure>
            <!-- /wp:video -->"""
        wp_tpl += f"""<!-- /wp:gallery -->"""
        return {"title":post.title, "content":wp_tpl,"status":"publish",
                "date_gmt":  datetime.strptime(post.stamp.split("_UTC")[0], "%Y-%m-%d_%H-%M-%S").strftime("%Y-%m-%d %H:%M:%S"),
                "tags":[all_tags[x] for x in post.hashtags]}

    # TODO: Cambiar aquí para ponerle la foto de portada
    def update_posts(self, subdomain, post_pairs, all_tags):
        cfg = self.config[subdomain]
        api_url = f"{self.protocol}://{subdomain}.{cfg['wp_domain']}/{self.post_api}"
        auth_obj = HTTPBasicAuth(cfg["wp_user"], cfg["wp_pwd"])
        results = []
        for pp, wpid in post_pairs:
            self.logger.debug(f"{'Updating' if wpid else 'Creating'} {pp.title or 'n/a'}")
            if self.status == "live":
                post_data = self.build_page(subdomain, pp, all_tags)
                api_url_f = f"{api_url}/{wpid}" if wpid else api_url
                self.logger.debug(f"Sending data to {api_url}")
                response = requests.post(f"{api_url_f}", auth=auth_obj, json=post_data)
                results.append((pp, response.json()["id"]))
                sleep(0.2)
        return results

    def get_posts(self, subdomain):
        cfg = self.config[subdomain]
        api_url = f"{self.protocol}://{subdomain}.{cfg['wp_domain']}/{self.post_api}"
        auth_obj = HTTPBasicAuth(cfg["wp_user"], cfg["wp_pwd"])
        response = requests.get(api_url, auth=auth_obj)
        return response.json()
