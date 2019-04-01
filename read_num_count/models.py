from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions


# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumDetail(models.Model):
    read_date = models.DateField(auto_now_add=True)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id', 'read_date')


class ReadNumExpandMethod():
    def get_read_time(self):  # 专门用来显示次数的，为什么不从blog.readtime.read_time取呢？
        try:
            con_typ = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=con_typ, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
