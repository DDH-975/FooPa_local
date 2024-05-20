from tinydb import TinyDB, Query, table
class UserModel:
    def __init__(self, path='C:/Users/user5/Desktop/db.json'):
        self.db = TinyDB(path)

    def upsert_user(self, user):
        if not self.db.search(Query().id == user.id):
            self.db.insert(table.Document(user.serialize(),doc_id=1))

    def get_user(self, user_id):
        user = self.db.search(Query().id == user_id)
        return UserData.deserialize(user[0])

    def remove_user(self, user_id):
        self.db.remove(Query().id == user_id)


class UserData:
    def __init__(self, user=None):
        if user:
            user_info = user['kakao_account']['profile']
            self.id = user['id']
            self.nickname = user_info['nickname']
            self.profile = user_info['profile_image_url']
            self.thumbnail = user_info['thumbnail_image_url']
        else:
            self.id = None
            self.nickname = None
            self.profile = None
            self.thumbnail = None

    def __str__(self):
        return "<UserData>(id:%s, nickname:%s)" \
            % (self.id, self.nickname)

    def serialize(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "profile": self.profile,
            "thumbnail": self.thumbnail
        }

    @staticmethod
    def deserialize(user_data):
        user = UserData()
        user.id = user_data['id']
        user.nickname = user_data['nickname']
        user.profile = user_data['profile']
        user.thumbnail = user_data['thumbnail']
        return user


    # 데이터베이스 파일 열기
    db = TinyDB('C:/Users/user5/Desktop/db.json')

    # 모든 데이터 가져오기
    all_data = db.all()

    # 데이터 출력
    for data in all_data:
        print(data)