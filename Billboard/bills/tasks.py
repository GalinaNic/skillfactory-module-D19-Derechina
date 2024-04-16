from celery import shared_task
from django.template.loader import render_to_string

from .models import Comment
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def comment_send_email(comment_id):
    comment = Comment.objects.get(id=comment_id)
    send_mail(
        subject=f'Новый отклик на объявление!',
        message=f'{comment.bill.author}, ! На ваше объявление есть новый отклик!\n'
                f'Прочитать отклик:\nhttp://127.0.0.1:8000/mycomments/{comment.bill.id}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[comment.bill.author.email, ],
    )


@shared_task
def comment_accept_send_email(comment_bill_id):
    comment = Comment.objects.get(id=comment_bill_id)
    send_mail(
        subject=f'Ваш отклик принят!',
        message=f'{comment.author}, aвтор объявления {comment.bill.title} принял Ваш отклик!\n'
                f'Посмотреть принятые отклики:\nhttp://127.0.0.1:8000/mycomments',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[comment.bill.author.email, ],
    )
