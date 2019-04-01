from django.urls import path
from .views import blog_detail, blog_list, blog_with_type, blog_with_date

urlpatterns = [
    path('blog/', blog_list, name='blog_list'),
    path('blog/<int:blog_id>', blog_detail, name='blog_detail'),  # int 后面不能有空格
    path('blog_type/<int:blog_type_id>', blog_with_type, name='blog_with_type'),
    path('blog/date/<int:year>/<int:month>', blog_with_date, name='blog_with_date')
    # blog_with_type.html中的blog.blog_with_type是不是在这里定义的，因为model中并没有这个属性 不对！他从blog_type中继承了这个属性
]