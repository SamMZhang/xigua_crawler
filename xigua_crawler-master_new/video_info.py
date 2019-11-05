import requests
import json
import sqlite3
import re
import os

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

    def __init__(self, values):
        self.video_id = values['video_id']
        self.user_id = values['user_id']
        self.title = values['title']
        self.upload_time = values['upload_time']
        self.avatar_path = values['avatar_path']
        self.avatar_url = values['avatar_url']
        self.abstract = values['abstract']

    def dump(self):
        """from insert a User object to database"""
        return (self.video_id, self.user_id,
                self.title, self.upload_time,
                self.avatar_path, self.avatar_url,
                self.abstract)

    def insert(self, obj, is_commit=True):
        """
        insert a object to database
        """
        if isinstance(obj, Video):
            self._insert_video(obj, is_commit)

    def _insert_video(self, video_obj, is_commit=True):
        global conn_video
        global cursor_video
        if not isinstance(video_obj, Video):
            raise TypeError('expect Video object')
        cursor_video.execute("INSERT INTO video VALUES(?,?,?,?,?,?,?)",
                             video_obj.dump())
        if is_commit:
            conn_video.commit()
            global db_dir
            print(str(db_dir) + " " + str(self.video_id) + " is inserted")


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

    def dump(self):
        """from insert a User object to database"""
        return (self.user_id, self.followers,
                self.watchers, self.nickname,
                self.avatar_path, self.avatar_url,
                self.des, self.is_pro)

    def insert(self, obj, is_commit=True):
        """
        insert a object to database
        """
        if isinstance(obj, User):
            self._insert_user(obj, is_commit)

    def _insert_user(self, user_obj, is_commit=True):
        self.conn = sqlite3.connect('User_info.db')
        self.cur = self.conn.cursor()
        if not isinstance(user_obj, User):
            raise TypeError('expect User object')
        self.cur.execute("INSERT INTO user VALUES(?,?,?,?,?,?,?,?)", user_obj.dump())
        # print("User ID:" + str(self.user_id) + " is inserted")
        if is_commit:
            self.conn.commit()


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
    # return 'https://www.ixigua.com/c/user/' + str(user_id)


def get_video_homepage_url(video_id):
    return "http://www.ixigua.com/group/{}&format=json".format(video_id)


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
        global v_id
        # video_json = json.JSONDecoder().decode(video_info)['video_info']
        video_id = v_id
        user_id = int(re.compile(r'mediaId: \'(.*)\'').findall(video_info)[0])
        title = "".join(re.compile(r'title: \'(.*)\'').findall(video_info))
        upload_time = ''
        avatar_path = ''
        avatar_url_user = "".join(re.compile(r'avatarUrl: \'(.*)\'').findall(video_info))
        abstract = re.compile(r'abstract: \'(.*)\'').findall(video_info)[0]
        return Video({
            'video_id': video_id,
            'user_id': user_id,
            'title': title,
            'upload_time': upload_time,
            'avatar_path': avatar_path,
            'avatar_url': avatar_url_user,
            'abstract': abstract
        })
    except Exception as e:
        print(str(e))


def parse_user_info(user_info):
    try:
        user_json = json.JSONDecoder().decode(user_info)['user_info']
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


def get_user_info(user_id='70460668473'):
    url = get_user_homepage_url(user_id)
    res = requests.get(url, headers=get_headers())
    user_obj = parse_user_info(res.text)
    return user_obj


def get_video_info(v_id='6515738164944962061'):
    url = get_video_homepage_url(v_id)
    res = requests.get(url, headers=get_headers())
    video_obj = parse_video_info(res.text)
    return video_obj


def get_file_name(f_dir):
    for files in os.walk(f_dir):
        return files


if __name__ == '__main__':
    # add video info into database
    files = ['F:\dataming\Data\Xigua_new\\200.113', 'F:\dataming\Data\Xigua_new\\200.111new']
    for file_dir in files:
        file_name = get_file_name(file_dir)
        for i in range(len(file_name[2])):
            file_name_one = file_name[2][i]
            db_dir = file_dir + '\\' + file_name_one
            # General insert method
            conn_video = sqlite3.connect(db_dir)
            print('db_id:' + str(db_dir))
            cursor_video = conn_video.cursor()
            conn_video.row_factory = sqlite3.Row
            sql = """select distinct video_id from 'tempor'"""
            cursor_video.execute(sql)
            video_ids = cursor_video.fetchall()
            # select video_ID for search video info in website
            for v_id in video_ids:
                # index = 0
                v_id = v_id[0]
                video_info = get_video_info(v_id)
                # user = User(user_info)
                try:
                    video_info.insert(obj=video_info, is_commit=True)
                except Exception as e:
                    print(str(e))
                    continue
