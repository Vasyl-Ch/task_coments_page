from django import forms
from captcha.fields import CaptchaField
from .models import Comment
from .sanitizer import sanitize_text

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "gif", "png"}
MAX_TXT_SIZE = 100 * 1024


class CommentForm(forms.ModelForm):
    captcha = CaptchaField(label="Введите капчу")

    class Meta:
        model = Comment
        fields = ["user_name", "email", "home_page", "text", "mediafile"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_text(self):
        raw = self.cleaned_data.get("text", "")
        return sanitize_text(raw)

    def clean_mediafile(self):
        file = self.cleaned_data.get("mediafile")
        if not file:
            return file

        name = file.name.lower()
        if "." in name:
            ext = name.split(".")[-1]
        else:
            ext = ""

        if ext in ALLOWED_IMAGE_EXTENSIONS:
            return file

        if ext == "txt":
            if file.size > MAX_TXT_SIZE:
                raise forms.ValidationError(f"TXT файл должен быть меньше 100 KB.")
            return file

        raise forms.ValidationError("Разрешены только JPG, GIF, PNG и TXT файлы.")
