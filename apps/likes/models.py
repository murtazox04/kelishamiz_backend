from django.db import models
from django.contrib.auth import get_user_model

from classifieds.models import Classified


User = get_user_model()


class ClassifiedLike(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Classified Like"
        verbose_name_plural = "Classified Likes"

    def __str__(self):
        return f"User: {self.user.full_name} - Classified: {self.classified.title}"
