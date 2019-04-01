from django import template
from django.contrib.contenttypes.fields import ContentType
from ..models import Comment
from ..forms import CommentForm
register = template.Library()


@register.simple_tag
def get_comments_count(obj):
    # get the comments_count from the 'obj' blog
    content_type = ContentType.objects.get_for_model(obj)
    comments_count = Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
    return comments_count


@register.simple_tag
def get_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, root=None)
    return comments.order_by('-comment_time')


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    data = {'content_type': content_type.model, 'object_id': obj.id, 'reply_comment_id': 0}
    comment_form = CommentForm(data)
    return comment_form
