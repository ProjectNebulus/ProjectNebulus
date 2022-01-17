class User:
    def __init__(self, username, email, password, avatar, courses, musiqueworld, bio, premium, staff, virtual_holidays):
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar
        self.courses = courses
        self.musique_world = musiqueworld
        self.bio = bio
        self.premium = premium
        self.staff = staff
        self.virtual_holidays = virtual_holidays
    def to_dictionary(self):
        the_dictionary = {
        "username" : self.username,
        "email": self.username,
        "password" : self.password,
        "avatar" : self.avatar,
        "courses" : self.courses,
        "musiqueworld" :self.musiqueworld,
        "bio": self.bio,
        "premium" : self.premium,
        "staff" : self.staff,
        "virtual_holidays" : self.virtual_holidays
        }
        return the_dictionary