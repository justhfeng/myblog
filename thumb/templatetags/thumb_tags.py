from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ThumbUpRecord
register = template.Library()


@register.simple_tag(takes_context=True)  # 引入界面中的user、request和'context_processors'
def get_thumb_status(context, obj):
    # 获取thumb的状态，输入用户，blog_pk，content_type，看看是否存在记录，若无记录，返回空；若有记录，返回字符串'active
    # 如果前端传入的blog_id变了怎么办？
    if not context['user'].is_authenticated:
        return ''
    content_type = ContentType.objects.get_for_model(obj)
    if ThumbUpRecord.objects.filter(user=context['user'], object_id=obj.pk, content_type=content_type).exists():
        # ThumbUpRecord.objects.filter(user=context['user'], object_id=obj.pk, content_type=content_type).exists()
        return 'active'
    else:
        return ''


@register.simple_tag
def get_thumb_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return ThumbUpRecord.objects.filter(object_id=obj.pk, content_type=content_type).count()


@register.simple_tag
def get_content_type_model(obj):
    content_type = ContentType.objects.get_for_model(obj).model
    return content_type

