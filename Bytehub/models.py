import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.course_name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    # the user needs to have chosen their course before being able to sign up.
    # this is for verification purposes
    user_image = models.ImageField(upload_to='profile_images', default='lebron.jpg')
    user_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, default=1)
    user_bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    # on_delete models.Cascade makes sure that if the author is deleted,
    # all the posts by that user is also removed
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=150)
    post_text = models.TextField(max_length=800)
    publication_date = models.DateTimeField("date published")
    post_upvotes = models.IntegerField(default=0)
    post_downvotes = models.IntegerField(default=0)

    def published_recently(self):
        return self.publication_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.post_title
