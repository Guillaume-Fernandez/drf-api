from django.db import models
from django.dispatch import receiver

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=20)
    is_done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    

@receiver(models.signals.post_init, sender=Task)
def remember_name(sender, instance, **kwargs):
    instance.previous_name = instance.name

@receiver(models.signals.pre_save, sender=Task)
def before_saving(sender, instance, **kwargs):
    pass

@receiver(models.signals.post_save, sender=Task)
def after_saving(sender, instance, **kwargs):
    pass

@receiver(models.signals.pre_delete, sender=Task)
def before_deleting(sender, instance, **kwargs):
    pass

@receiver(models.signals.post_delete, sender=Task)
def after_deleting(sender, instance, **kwargs):
    pass