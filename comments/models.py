from django.db import models
from config.validators import validate_latin_alphanumeric


class Comment(models.Model):
    user_name = models.CharField(
        max_length=100, validators=[validate_latin_alphanumeric], verbose_name="Имя"
    )
    email = models.EmailField(verbose_name="Email")
    home_page = models.URLField(blank=True, null=True, verbose_name="Главная страница")
    text = models.TextField(verbose_name="Ваш комментарий")
    mediafile = models.FileField(
        upload_to="attachments/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name="Прикреплённый файл",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="Основной комментарий",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.user_name} | {self.created_at:%Y-%m-%d %H:%M}"

    def is_root(self):
        return self.parent is None
