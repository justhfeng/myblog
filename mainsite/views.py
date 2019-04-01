from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Blog, BlogType
from user.forms import LoginForm
from read_num_count.utils import read_num_add, seven_day_read_num_add, hot_read_num_details_today, \
    hot_read_num_details_yesterday, hot_read_blogs_7_days


def home(request):
    context = {}
    ct = ContentType.objects.get_for_model(Blog)  # content_type
    read_nums, dates = seven_day_read_num_add(ct)

    hot_blogs_7_days = cache.get('hot_blogs_7_days')
    if hot_blogs_7_days is None:
        hot_blogs_7_days = hot_read_blogs_7_days(ct)
        cache.set('hot_blogs_7_days', hot_blogs_7_days, 60)
        print('set cache')
    else:
        print('use cache')
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['hot_read_details_today'] = hot_read_num_details_today(ct)
    context['hot_read_details_yesterday'] = hot_read_num_details_yesterday(ct)
    context['hot_blogs_7_days'] = hot_blogs_7_days
    # context['hot_blogs_7_days'] = hot_read_blogs_7_days(ct)
    # context['hot_read_details_7_days'] = hot_read_num_details_7_days(ct)
    return render(request, 'home.html', context)


def blog_list(request):
    page_num = request.GET.get('page', 1)
    blogs_all = Blog.objects.filter(is_deleted=False)
    context = return_context(blogs_all, page_num)
    # 为了显示一个评论数而得到content_type,进而根据blog.id得到对应comments及其数量，代码量非常大，因此可以选择用
    return render(request, 'mainsite/blog_list.html', context)


def blog_detail(request, blog_id):  # 这个blog_id是谁给这个方法的？ 一个html页面一定要对应一个同名的方法吗？联系html和方法的途径就是传一个context过去吗？
    context = {}
    blog = get_object_or_404(Blog, pk=blog_id)
    if blog.is_deleted:
        return render(request, 'error.html', {'message': '该文章已被删除', 'redirect_to': '/'})
    last_blog = Blog.objects.filter(created_time__lt=blog.created_time, is_deleted=False).first()
    next_blog = Blog.objects.filter(created_time__gt=blog.created_time, is_deleted=False).last()
    cookie_key = read_num_add(request, blog)
    # content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(object_id=blog_id, content_type=content_type, root=None)
    # data = {'content_type': content_type.model, 'object_id': blog_id, 'reply_comment_id': 0}
    # comment_form = CommentForm(data)
    # context['comment_form'] = comment_form  # 提交以后，界面自动刷新吗？
    # context['comments'] = comments.order_by('-comment_time')
    context['blog'] = blog
    context['last_blog'] = last_blog
    context['next_blog'] = next_blog
    context['login_modal_form'] = LoginForm()
    request = render(request, 'mainsite/blog_detail.html', context)
    request.set_cookie(cookie_key, "True")
    return request


def blog_with_type(request, blog_type_id):
    type_page_num = request.GET.get('page', 1)
    blog_type = get_object_or_404(BlogType, pk=blog_type_id)
    blogs_with_type = Blog.objects.filter(blog_type=blog_type)
    context = return_context(blogs_with_type, type_page_num)
    context['blog_type'] = blog_type
    return render(request, "mainsite/blog_with_type.html", context)


def blog_with_date(request, year, month):
    page_num = request.GET.get('page', 1)
    context = {}
    blogs_all = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = return_context(blogs_all, page_num)
    return render(request, 'mainsite/blog_with_date.html', context)


# 输入blogs和显示页数，输出包含当页的博客，底部导航数据
def return_context(blogs, page_num):
    context = {}
    paginator = Paginator(blogs, settings.BLOG_NUM_PER_PAGE)
    blogs_page = paginator.get_page(page_num)
    context['blog_list'] = blogs_page
    # context['blog_types'] = BlogType.objects.all()
    # 生成附近2个页码
    blog_range = [x for x in range(int(blogs_page.number) - 2, int(blogs_page.number) + 3) if
                  0 < x <= blogs_page.paginator.num_pages]
    # 增加第一页和最后一页
    if blog_range[0] != 1:
        blog_range.insert(0, 1)
    if blog_range[-1] != blogs_page.paginator.num_pages:
        blog_range.append(blogs_page.paginator.num_pages)
    # 增加...
    if len(blog_range) > 1:  # 防止出现该类别下的博客页面只有一页，导致blog_range[1]不存在/或者先添加...然后再增加第一页和最后一页
        if blog_range[1] - blog_range[0] > 1:
            blog_range.insert(1, '...')
        if blog_range[-1] - blog_range[-2] > 1:
            blog_range.insert(-1, '...')
    context['blog_range'] = blog_range

    # 统计每个blog_type对应的博客数量
    # 方法1
    # blog_type_list = []
    # for blog_type in BlogType.objects.all():
    #     blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    #     blog_type_list.append(blog_type)
    # 方法2
    blog_type_list = BlogType.objects.annotate(blog_count=Count("blog"))
    context['blog_type_list'] = blog_type_list

    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    # 统计每个blog_dates对应的博客数量
    # 方法1
    blog_date_dic = {}
    for blog_date in blog_dates:
        blog_date_dic[blog_date] = Blog.objects.filter(created_time__year=blog_date.year,
                                                       created_time__month=blog_date.month).count()
    context['blog_dates'] = blog_date_dic
    # 方法2

    return context
