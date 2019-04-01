from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm


# 利用自定义表单实现的增加评论功能
# Create your views here.
# def add_comment(request):
#     referer = request.META.get('HTTP_REFERER', reverse('home'))
#     user = request.user
#     if user.is_authenticated is None:
#         return render(request, 'error.html', {'message': '用户未登陆', 'redirect_to':referer})
#     text = request.POST.get('text', '').strip()
#     if text == '':
#         return render(request, 'error.html', {'message': '输入文字为空', 'redirect_to':referer})
#
#     try:
#         content_type = request.POST.get('content_type', '')
#         object_id = int(request.POST.get('object_id', ''))
#         content_object = ContentType.objects.get(model=content_type).model_class().objects.get(id=object_id)
#     except Exception as e:
#         return render(request, 'error.html', {'message': '对象错误', 'redirect_to':referer})
#     comment = Comment()
#     comment.user = user
#     comment.comment_text = text
#     comment.content_object = content_object  # 不用添加object_id和content_type吗？
#     comment.save()
#     return redirect(referer)

def add_comment(request):
    # 利用Django Form实现的增加评论内容，并将除form.is_valid()功能以外放入forms.py当中
    comment_form = CommentForm(request.POST, user=request.user)  # 记得在此处添加user，为什么在views当中不添加呢？可不可以？
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    data = {}
    if comment_form.is_valid():  # 可以确认用户框是否为空，并自动执行对应Form当中的clean方法
        comment = Comment()
        comment.author = comment_form.cleaned_data['user']
        comment.comment_text = comment_form.cleaned_data['comment']\
            .strip().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()  # 去除首位换行\空格
        comment.content_object = comment_form.cleaned_data['content_object']  # 已将content_object的获取和验证放入到CommentForm当中
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            if parent.root:
                comment.root = parent.root
            else:
                comment.root = parent
            comment.reply_to = parent.author
            comment.parent = parent
        comment.save()

        # 发送邮件通知被回复或被评论的用户
        comment.send_notification_via_email()

        # 返回数据,不直接刷新界面，而是利用ajax在该界面上添加内容
        # 用户界面要显示用户名，发表时间和评论内容
        data['status'] = 'success'
        data['username'] = comment.author.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()  # timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')
        data['comment_text'] = comment.comment_text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        data['pk'] = comment.id  # data中的数据只用在ajax中，用于实时显示回复(reply(id))和root_(id)
        data['comments_count'] = Comment.objects.filter(object_id=comment_form.cleaned_data['object_id']).count()
        if comment.parent:
            data['reply_to_username'] = comment.parent.author.get_nickname_or_username()
        else:
            data['reply_to_username'] = ''
        data['root_pk'] = comment.root.id if comment.root else ''  # 设计root_id的意义是为了增加回复的定位
        # return redirect(referer)  # 不直接刷新界面，而是利用ajax在该界面上添加内容
    else:
        data['status'] = 'error'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
    # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
    # raise comment_form.ValidationError('请重新输入！')


