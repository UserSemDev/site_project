import bcrypt
from django.utils import timezone
from mongoengine import Document, StringField, EmailField, DateTimeField


class User(Document):
    username = StringField(max_length=150, required=True, unique=True)
    email = EmailField(required=True, unique=True)
    role = StringField(choices=["user", "admin"], default="user")
    password = StringField(required=True)
    date_joined = DateTimeField(default=timezone.now)
    last_login = DateTimeField()

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password.encode("utf-8"))

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.password.startswith("$2b$"):
            self.set_password(self.password)

        if not self.date_joined:
            self.date_joined = timezone.now()
        super().save(*args, **kwargs)
