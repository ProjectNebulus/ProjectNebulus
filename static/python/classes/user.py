class User:
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id")
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.avatar = kwargs.get('avatar') or ''
        self.courses = kwargs.get('courses') or []
        self.musiqueworld = kwargs.get('musiqueworld') or []
        self.bio = kwargs.get('bio') or ''
        self.premium = kwargs.get('premium') or '0'
        self.staff = kwargs.get('staff') or '0'
        self.virtual_holidays = kwargs.get('virtual_holidays') or []

    def to_dictionary(self):
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
