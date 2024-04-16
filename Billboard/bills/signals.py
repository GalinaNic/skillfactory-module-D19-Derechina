# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
#
# from Billboard.settings import SITE_URL, DEFAULT_FROM_EMAIL
# from .models import Bill, Comment
#
#
# @receiver(post_save, sender=Comment)
# def get_comment(sender, instance, created, **kwargs):
#     if created:
#         destination = [instance.comment_bill.author.email]
#         title = 'Новый отклик на Ваше объявление!'
#         text = f'Пользователь {instance.author.username} оставил отклик на Ваше объявление:'
#
#     else:
#         destination = [instance.author.email]
#         title = 'Ваш отклик принят!'
#         text = f'Пользователь {instance.comment_bill.author.username} принял Ваш отклик:'
#
#     send_notification_about_comment(instance, title, text, destination)
#
#
# def send_notification_about_comment(comment, title, text, destination):
#     html_content = render_to_string(
#         'email.html',
#         {
#             'title': title,
#             'bill': comment.comment_bill.title,
#             'comment': comment.content,
#             'text': text,
#             'link': f'{SITE_URL}/bill/{comment.comment_bill.id}',
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         from_email=DEFAULT_FROM_EMAIL,
#         to=destination
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(post_save, sender=Bill)
# def notify_about_new_post(sender, instance, created, **kwargs):
#     if created:
#         category = instance.category
#         subscribers_emails = []
#         subscribers = category.subscribers.all()
#         for subscriber in subscribers:
#             subscribers_emails += [subscriber.email]
#         title = 'Новое объявление в вашей любимой категории!'
#         text = f'Пользователь {instance.author.username} добавил новое объявление:'
#
#         send_notification_new_post(instance, title, text, subscribers_emails)
#
#
# def send_notification_new_post(bill, title, text, destination):
#     html_content = render_to_string(
#         'email.html',
#         {
#             'title': title,
#             'advert': bill.title,
#             'respond': None,
#             'text': text,
#             'link': f'{SITE_URL}/advert/{bill.id}',
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         from_email=DEFAULT_FROM_EMAIL,
#         to=destination
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Bill
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import mail_managers


@receiver(post_save, sender=Bill)
def create_bill(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.title} {instance.created.strftime("%Y-%M-%d")}')


@receiver(post_save, sender=Comment)
def send_message_comment(sender, instance, created, **kwargs):
    if created and instance.user.email:
        print(f'''Пользователь {instance.user.email}, откликнулся на ваше объявление - '{instance.comment_bill.title}' ''')

        html_content = render_to_string('comment_created_email.html', {'instance': instance, })

        msg = EmailMultiAlternatives(
            subject=f'Отклик на пост - {instance.text}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.comment_bill.author.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
