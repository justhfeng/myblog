from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.contenttypes.fields import ContentType
from django.db.models import ObjectDoesNotExist
from .models import ThumbUpRecord


def error_message(code, message):
    data = dict()
    data['status'] = 'FAIL'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


# Create your views here.
def thumb_up(request):
    # 后端要做哪些内容？
    # 判断用户是否登陆，若用户已登陆：
    #   判断用户是否已评论，1. 若用户未评论：更新thumb信息；2.若用户已评论：删除thumb信息。返回登陆成功信息和点赞总数
    # 若用户未登陆：
    #   返回用户未登陆
    # 输入内容：user\content_type\blog_id
    # 如何获取从ajax导入的数据
    user = request.user
    if not user.is_authenticated:
        return error_message(400, 'You are not logged in!')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        # 确认是否存在此blog
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_object = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return error_message(401, 'Blog/Comment does not exit!')

    # 有可能前后端不匹配
    # 先把主要功能（此处为创建记录）给写完，然后再补上用户是否登陆和对象（博客）是否存在的判断！！！

    data = dict()
    thumb_model, created = ThumbUpRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
    if created:
        thumb_model.save()
        data['message'] = 'created'
    else:
        thumb_model.delete()
        data['message'] = 'deleted'
    data['thumbs_count'] = ThumbUpRecord.objects.filter(content_type=content_type, object_id=object_id).count()
    data['status'] = 'SUCCESS'
    return JsonResponse(data)
