from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from news.models import PostCategory
from .tasks import inform_about_new_post



# def send_notifications(preview, pk, title, subscribers):
#     for subscriber in subscribers:
#         html_content = render_to_string(
#             'post_created_email.html',
#             {
#                 'username': subscriber.username,
#                 'text': preview,
#                 'link': f'{settings.SITE_URL}/news/{pk}'
#             }
#         )
#
#         msg = EmailMultiAlternatives(
#             subject=title,
#             body='',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[subscriber.email],
#         )
#
#         msg.attach_alternative(html_content, 'text/html')
#         msg.send()
# #
#
@receiver(m2m_changed, sender=PostCategory, dispatch_uid='my_unique_identifier')
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_users = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_users += [s for s in subscribers]

        inform_about_new_post.delay(instance.pk)




