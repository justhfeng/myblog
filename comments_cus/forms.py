from django import forms
from django.contrib.contenttypes.models import ContentType
from ckeditor.widgets import CKEditorWidget
from .models import Comment


# 评论表单
class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.CharField(widget=forms.HiddenInput)
    comment = forms.CharField(label='请提交评论', widget=CKEditorWidget(config_name='comment_ckeditor'),
                              error_messages={'required': '评论内容不能为空'})
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))
    # 为什么这个地方要设置一个字典？令id=reply_comment_id
    # username = forms.CharField(widget=forms.HiddenInput) 这种方法是错误的，因为需要将user传递给内部，而非根据username进行判断
    # user = User.objects.get(username=username)

    # 这段话是什么意思
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证用户登陆情况
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登陆')
        # 验证评论对象
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        # 判断是否具有对应博客
        try:
            content_object = ContentType.objects.get(model=content_type).model_class().objects.get(id=object_id)
        except Exception as e:
            raise forms.ValidationError('无对应博客内容！')
        self.cleaned_data['content_object'] = content_object
        return self.cleaned_data

    def clean_reply_comment_id(self):  # 返回什么？ reply_comment_id, return reply_comment_id和return self.cleaned_data有什么区别
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('无对应回复内容')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复内容不存在！')
        return reply_comment_id  # 这种是固定格式吗？
