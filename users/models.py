from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
