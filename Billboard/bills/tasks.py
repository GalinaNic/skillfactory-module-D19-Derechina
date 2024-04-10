from celery import shared_task
from .models import Comment
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def respond_send_email(respond_id):
    respond = Comment.objects.get(id=respond_id)
    send_mail(
        subject=f'Новый отклик на объявление!',
        message=f'{respond.bill.author}, ! На ваше объявление есть новый отклик!\n'
                f'Прочитать отклик:\nhttp://127.0.0.1:8000/comments/{respond.bill.id}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[respond.bill.author.email, ],
    )


@shared_task
def respond_accept_send_email(comment_id):
    respond = Comment.objects.get(id=comment_id)
    send_mail(
        subject=f'Ваш отклик принят!',
        message=f'{respond.author}, aвтор объявления {respond.bill.title} принял Ваш отклик!\n'
                f'Посмотреть принятые отклики:\nhttp://127.0.0.1:8000/comments',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[respond.bill.author.email, ],
    )
