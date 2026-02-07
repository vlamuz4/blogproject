from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Post

@receiver(post_save, sender=Post)
def clear_cache(sender, **kwargs):
    cache.clear()
