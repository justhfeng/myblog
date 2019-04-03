import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadNumDetail
from mainsite.models import Blog


# 计数加一
def read_num_add(request, obj):
    con_typ = ContentType.objects.get_for_model(obj)
    cookie_key = "%s_%s_read" % (con_typ.model, obj.pk)
    date_now = timezone.now().date()
    if not request.COOKIES.get(cookie_key):
        # if ReadNum.objects.filter(content_type=con_typ, object_id=obj.pk).count():
        #     # 存在记录
        #     readnum = ReadNum.objects.get(content_type=con_typ, object_id=obj.pk)
        #     # readnum = get_object_or_404(ReadTime, blog=blog)  # ReadTime.objects.filter(blog=blog)
        # else:
        #     # 不存在记录，创建一个
        #     readnum = ReadNum(content_type=con_typ, object_id=obj.pk)  # 这是创建一个的意思吗？
        # 总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=con_typ, object_id=obj.pk)
        readnum.read_num += 1  # 那如果没有呢？
        readnum.save()

        # 每天阅读数+1
        readnum_day, created = ReadNumDetail.objects.get_or_create(content_type=con_typ, object_id=obj.pk, read_date=date_now)
        readnum_day.read_num += 1  # 那如果没有呢？
        readnum_day.save()
    return cookie_key


# 返回对应content_type和日期的阅读量，即统计每一天的阅读量
def seven_day_read_num_add(ct):
    date_now = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = date_now - datetime.timedelta(days=i)  # 得到所需日期
        read_details = ReadNumDetail.objects.filter(content_type=ct, read_date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
        dates.append(date.strftime('%m/%d'))  # 将日期转换为字符串
    # 统计每个日期下的阅读数量
    return read_nums, dates


# 统计今天热门阅读量
def hot_read_num_details_today(ct):
    today = timezone.now().date()
    read_details = ReadNumDetail.objects.filter(content_type=ct, read_date=today)
    return read_details.order_by('-read_num')[:7]


# 统计昨天热门阅读量
def hot_read_num_details_yesterday(ct):
    yesterday = timezone.now().date()-datetime.timedelta(days=1)
    read_details = ReadNumDetail.objects.filter(content_type=ct, read_date=yesterday)
    return read_details.order_by('-read_num')[:7]   # 为什么计数为0的数据不会被传进去？


# 统计前7天热门阅读量(此方法无法获取object的标题，因此弃用)
# def hot_read_num_details_7_days(ct):
#     today = timezone.now().date()
#     seven_days_before_today = today - datetime.timedelta(days=7)
#     # values的作用
#     read_details = ReadNumDetail.objects \
#                                 .filter(content_type=ct, read_date__gte=seven_days_before_today, read_date__lt=today)\
#                                 .values('content_type', 'object_id')\
#                                 .annotate(read_num_sum=Sum('read_num'))\
#                                 .order_by('-read_num_sum')
#     return read_details[:7]


# 统计前7天热门博客
def hot_read_blogs_7_days(ct):
    today = timezone.now().date()
    seven_days_befor_today = today - datetime.timedelta(days=7)
    hot_blogs = Blog.objects\
                        .filter(read_detail__content_type=ct, read_detail__read_date__gte=seven_days_befor_today, read_detail__read_date__lt=today)\
                        .values('id', 'title')\
                        .annotate(read_num_sum=Sum('read_detail__read_num'))\
                        .order_by('-read_num_sum')
    hot_blogs = Blog.objects.filter(read_detail__content_type=ct, read_detail__read_date__gte=seven_days_befor_today, read_detail__read_date__lt=today).values('id', 'title').annotate(read_num_sum=Sum('read_detail__read_num')).order_by('-read_num_sum')
    return hot_blogs[:7]




