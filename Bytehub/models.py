import datetime
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()


# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.course_name


class Profile(models.Model):
    # one to one relationship so the user can access profile attributes as well
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # the user needs to have chosen their course before being able to sign up.
    # this is for verification purposes
    user_image = models.ImageField(upload_to='profile_images', default='lebron.jpg')
    user_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, default=1)
    user_bio = models.TextField(default="This is the my bio.")
    display_name = models.TextField(default="Anonymous User")
    bookmarks = models.ManyToManyField('Post', related_name='bookmarked_by', blank=True)
    connected_users = models.ManyToManyField('Profile', related_name='connections', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    # on_delete models.Cascade makes sure that if the author is deleted,
    # all the posts by that user is also removed
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=150)
    post_text = RichTextField()
    publication_date = models.DateTimeField("date published", auto_now_add=True)
    post_upvotes = models.IntegerField(default=0)
    post_downvotes = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def published_recently(self):
        return self.publication_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_text = RichTextField()
    publication_date = models.DateTimeField("date published", auto_now_add=True)
