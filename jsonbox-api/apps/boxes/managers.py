from django.contrib.auth.models import User
from django.db.models import Manager
from django.utils.text import slugify
from rest_framework.authtoken.models import Token


class BoxManager(Manager):
    def create_for_username(self, box_name, username):
        name = slugify(box_name)
        user, _ = User.objects.get_or_create(username=username)
        token, _ = Token.objects.get_or_create(user=user)
        return self.create(name=name, token=token)
