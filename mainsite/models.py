from django.db import models
from django.contrib.auth.admin import User
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from read_num_count.models import ReadNumExpandMethod, ReadNumDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


# Create your models here.
class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=30)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_detail = GenericRelation(ReadNumDetail)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    '''
    def get_read_time(self):  # 专门用来显示次数的，为什么不从blog.readtime.read_time取呢？
        try:
            con_typ = ContentType.objects.get_for_model(Blog)
            readnum = ReadNum.objects.get(content_type=con_typ, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    '''

    def __str__(self):
        return "<title: %s>" % self.title

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_id': self.pk})  # 可以到urls.py里面看是blog_id还是blog_pk

    class Meta:
        ordering = ['-created_time']


# class ReadTime(models.Model):
#     read_time = models.IntegerField(default=0)
#     blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
