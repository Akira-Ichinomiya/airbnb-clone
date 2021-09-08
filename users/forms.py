from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                print("비밀번호 에러")
                self.add_error(None, forms.ValidationError("입력한 정보가 일치하지 않습니다."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("입력한 정보가 일치하지 않습니다."))


class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        user.username = email
        user.set_password(password)
        print("유저를 저장합니다.")
        user.save()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(email=email)
            if user:
                print("에러발생 이메일")
                self.add_error("email", forms.ValidationError("같은 이메일이 이미 존재합니다."))
        except:
            pass

