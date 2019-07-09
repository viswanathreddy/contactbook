from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    # any other fields add here
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(blank=True)

    class Meta:
        ordering = ('updated_at',)
        unique_together = (('created_by', 'email'),)
        index_together = [['created_by', 'name'], ]

    # def __str__(self):
    #     return str(self.id) + " " + self.email

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Contact, self).save(*args, **kwargs)
