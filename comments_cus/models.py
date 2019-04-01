import threading
from django.db import models
from django.contrib.auth.admin import User
from django.contrib.contenttypes.fields import ContentType, GenericForeignKey
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from mainsite.models import Blog


# 多线程处理发送邮件
class SendNotificationViaEmail(threading.Thread):
    def __init__(self, subject, email_content, email, fail_silently=False):
        self.subject = subject
        self.email_content = email_content
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, '', settings.EMAIL_HOST_USER, [self.email], fail_silently=self.fail_silently,
                  html_message=self.email_content)


# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # null=True的意思是存储一个NULL在数据库，利用related_name(.root_comment)查找对应评论
    root = models.ForeignKey('self', null=True, related_name='root_comment', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, related_name='parent_comment', on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, null=True, related_name='replies', on_delete=models.CASCADE)  # 不能直接parent.user吗？

    def __str__(self):  # 将类的实例变成字符串
        return self.comment_text

    def send_notification_via_email(self):
        # 评论收到回复，发送邮件给comment.parent.author.email，内容就是自己的内容comment.parent.comment_text+回复内容comment.comment_text
        # 判断是评论还是回复
        # 首先需要判断用户是否具有对应的邮箱地址，否则不发邮件
        # 缺点：就是会卡一下，怎么解决
        if self.parent:
            # 回复
            subject = '您的评论有新回复'
            email = self.parent.author.email
        else:
            # 评论
            subject = '您的博客有新的评论'
            email = self.author.email
        if email != '':
            context = dict()
            context['comment_author_name'] = self.author.get_nickname_or_username()
            context['comment_text'] = self.comment_text  # self.comment_text评论内容本来就有p标签，
            print(self.comment_text)
            context['link'] = self.content_object.get_url()
            context['link_label'] = '点击查看'
            email_content = render(None, 'comments_cus/email_content.html', context).content.decode('utf-8')
            # email_content = render_to_string('comments_cus/email_content.html', context)

            # email_content = '您收到"%s"的评论:%s\n<a href="%s">%s</a>' % (self.author.get_nickname_or_username(),
            # self.comment_text, self.content_object.get_url(), '点击查看')
            send_notification = SendNotificationViaEmail(subject, email_content, email)
            send_notification.start()





