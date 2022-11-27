from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER


def send_email(subject, message, to):
    print(to)
    print(isinstance(to, tuple))
    print([to])
    recipient_list = to if isinstance(to, (tuple, list)) else [to]
    send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_list,
              fail_silently=False)


def get_pagination(request, object_list, per_page):
    paginator = Paginator(object_list=object_list, per_page=per_page)
    page = request.GET.get('page')
    try:
        elements = paginator.page(page)
    except PageNotAnInteger:
        elements = paginator.page(1)
    except EmptyPage:
        elements = paginator.page(paginator.num_pages)
    return elements
