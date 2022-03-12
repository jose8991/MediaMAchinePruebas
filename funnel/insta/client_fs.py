import os
import re
import json
import lzma
import random
from dataclasses import dataclass
from nltk.tokenize import regexp_tokenize, sent_tokenize


@dataclass
class Post:
    idx:str
    user:str
    stamp:str
    title:str
    description:str
    likes:int
    jpgs:list
    mp4s:list
    hashtags:list
    tagged:list
    likers:dict
    comments:list
    vid_pos_abs:int
    vid_pos_rel:int

    @classmethod
    def from_set(cls, user, stamp, post_set, post_repo_path = "../insta/scripts"):
        text = [x for x in post_set if x.endswith("txt")] or ""
        if text:
            text = open(f"{post_repo_path}/{user}/{text[0]}").read() if text else ""
        title = sent_tokenize(text) or ""
        if title:
            title = title[0]
            if len(title) > 50:
                cand_title = re.split("[¿?¡!.,:\n]",title)
                title = cand_title[0]
        text = re.sub("\n", " <br />", text)
        idx = re.sub("[^a-zA-Z ]","",title).replace(" ","-") if title else "no-id"

        #TODO:Rewrite this
        likes = 0
        jpgs = [x for x in post_set if x.endswith("jpg")]
        mp4s = [x for x in post_set if x.endswith("mp4")]
        hashtags = [re.sub("[^\w#]", "", w) for w in regexp_tokenize(text.replace("#", " #"), pattern=r"\s|[\.,;'!&-<>]", gaps=True) if "#" in w and w[-1] != "#"]
        tagged = [re.sub("[^\w@]", "", w) for w in regexp_tokenize(text, pattern=r"\s|[\.,;'!&-]", gaps=True) if "@" in w and w[-1] != "@"]
        meta = [x for x in post_set if x.endswith(".xz")]
        comments = [x for x in post_set if x.endswith("comments.json")]

        vid_pos_abs = -1
        if mp4s:
            vid_pos_abs = 0
            first_vid = re.findall("_(\d+)\.mp4", mp4s[0])
            if first_vid:
                vid_pos_abs = int(first_vid[0])

        likers = []
        if meta:
            meta = json.load(lzma.open(post_repo_path + f"/{user}/" + meta[0],
                                       mode='rt', encoding='utf-8'))
            if meta:
                if "edge_media_preview_like" in meta["node"]:
                    likes = meta["node"]["edge_media_preview_like"]["count"]
                if "iphone_struct" in meta["node"] and "likers" in meta["node"]["iphone_struct"]:
                    likers = meta["node"]["iphone_struct"]["likers"]

        if comments:
            with open(post_repo_path + f"/{user}/" + comments[0]) as f:
                comments = json.load(f)

        return Post(idx,user,stamp,title,text,likes,jpgs, mp4s, hashtags, tagged, likers, comments, vid_pos_abs,
                    max(0,0 if not jpgs else (vid_pos_abs+1)/(len(jpgs)+len(mp4s))))


class InstaPostManager:
    def __init__(self, path):
        self.path = path

    def get_all_posts(self):
        all_post_names = {}
        for user in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path,user)):
                all_post_names[user] = {}
                for post in self.get_post_names(user, remove_extension=True):
                    all_post_names[user][post] = Post.from_set(user, post,
                                                               self.get_post_names_starting_with(user, post))
        return all_post_names

    def get_post_names(self, user, starting_with="", remove_extension=False, include_meta=False):
        all_pref = []
        sample = sorted(os.listdir(f"{self.path}/{user}"))
        for s in sample:
            x = s
            if remove_extension and user not in x:
                x = s.split(".",1)[0]
                x = x if x.endswith("UTC") else x.rsplit("_",1)[0]
            if (not starting_with or x.startswith(starting_with)) and \
                    (include_meta or (x!="id" and user not in x)) and \
                    (x not in (":tagged")) and (not x.startswith("iter")):
                all_pref.append(x)
        return list(set(all_pref))

    def get_random_post_name(self, user):
        return self.get_post_names(starting_with=random.sample(self.posts,1)[0], remove_extension=False)

    def get_post_names_starting_with(self, user, post):
        return self.get_post_names(user, starting_with=post, remove_extension=False)

    def get_posts(self, user, starting_with=""):
        return [Post.from_set(user, p, self.get_post_names_starting_with(user, p))
                for p in sorted(self.get_post_names(user, starting_with, remove_extension=True))]
