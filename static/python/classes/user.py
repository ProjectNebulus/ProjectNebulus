# A user object - Will be used in the API
class User:
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id")
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.avatar = kwargs.get('avatar', '')
        self.courses = kwargs.get('courses', [])
        self.musiqueworld = kwargs.get('musiqueworld', [])
        self.bio = kwargs.get('bio', '')
        self.premium = kwargs.get('premium', '0')
        self.staff = kwargs.get('staff', '0')
        self.virtual_holidays = kwargs.get('virtual_holidays', [])

    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.username,
            "password": self.password,
            "avatar": self.avatar,
            "courses": self.courses,
            "musiqueworld": self.musiqueworld,
            "bio": self.bio,
            "premium": self.premium,
            "staff": self.staff,
            "virtual_holidays": self.virtual_holidays
        }
