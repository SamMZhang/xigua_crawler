import requests
import json
import sqlite3

ua_index = 0

class Video:
    """
    CREATE TABLE video (
        video_id TEXT NOT NULL,
        user_id TEXT,
        title TEXT,
        upload_time DATETIME,
        avatar_path TEXT,
        avatar_url TEXT,
        des TEXT,
        PRIMARY KEY (video_id)
    )
    """

    def __init__(self, video_id, user_id, title, upload_time, avatar_path, avatar_url, des):
        self.video_id = video_id
        self.user_id = user_id
        self.title = title
        self.upload_time = upload_time
        self.avatar_path = avatar_path
        self.avatar_url = avatar_url
        self.des = des


class User:
    """
    CREATE TABLE user (
        user_id TEXT NOT NULL,
        followers INTEGER,
        watchers INTEGER,
        nickname TEXT,
        avatar_path TEXT,
        avatar_url TEXT,
        des TEXT,
        is_pro INTEGER,
        PRIMARY KEY (user_id)
    )
    """

    def __init__(self, values):
        self.user_id = values['user_id']
        self.followers = values['followers']
        self.watchers = values['watchers']
        self.nickname = values['nickname']
        self.avatar_path = values['avatar_path']
        self.avatar_url = values['avatar_url']
        self.des = values['des']
        self.is_pro = values['is_pro']

    def insert2db(self):
        pass


def get_ua():
    global ua_index
    mobile_ua = [
        "User-Agent,Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "User-Agent,Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "User-Agent,Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "User-Agent, Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "User-Agent, MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "User-Agent, Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "User-Agent, Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "User-Agent, Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "User-Agent, Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "User-Agent, Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "User-Agent, Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "User-Agent, UCWEB7.0.2.37/28/999",
        "User-Agent, NOKIA5700/ UCWEB7.0.2.37/28/999",
        "User-Agent, Openwave/ UCWEB7.0.2.37/28/999",
        "User-Agent, Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"]
    ua_index = (ua_index + 1) % len(mobile_ua)


def get_headers():
    return {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'user-agent': get_ua()
    }


def get_user_homepage_url(user_id):
    return "https://m.ixigua.com/video/app/user/home/?to_user_id={}&format=json".format(user_id)


def get_video_homepage_url(video_id):
    return "http://m.toutiaoimg.cn/i{}/#mid=1603802501009411".format(video_id)


def parse_user_info(user_info):
    try:
        user_json = json.JSONEncoder().encode(user_info)['user_info']
        user_id = user_json['user_id']
        user_name = user_json['name']
        followers_count = user_json['followers_count']
        avatar_url = user_json['avatar_url']
        is_verified = user_json['user_verified']
        following_count = user_json['following_count']
        description = user_json['description']
        return User({
            'user_id': user_id,
            'followers': followers_count,
            'watchers': following_count,
            'des': description,
            'avatar_path': '',
            'avatar_url': avatar_url,
            'nickname': user_name,
            'is_pro': is_verified,
        })
    except Exception as e:
        print(str(e))


def parse_video_info(video_info):
    def parse_title():
        pass

    def parse_upload_time():
        pass

    def parse_avatar_path():
        pass

    def parse_avatar_url():
        pass

    def parse_des():
        pass

    try:
        pass
    except Exception as e:
        print(str(e))


def get_user_info(user_id='70460668473'):
    url = get_user_homepage_url(user_id)
    res = requests.get(url, headers=get_headers())
    user = parse_user_info(res.text)
    return user


def get_video_info(video_id='6515738164944962061'):
    url = get_video_homepage_url(video_id)
    res = requests.get(url, headers=get_headers())
    # video = parse_video_info(res.text)
    # return video


