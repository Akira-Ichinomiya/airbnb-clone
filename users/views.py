import os
import requests
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView
from . import models, forms


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("core:home")

    initial = {
        "first_name": "Lee",
        "last_name": "Heesu",
        "email": "heesu0730@nate.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.save()
        # to do: add success message
        return redirect(reverse("core:home"))
    except models.User.DoesNotExist:
        # to do: add error meesage
        return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class githubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        if code is not None:
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            result_json = result.json()
            error = result_json.get("error", None)
            if error:
                raise githubException()
            else:
                access_token = result_json.get("access_token")
                api_request = requests.get(
                    "https://api.github.com/user",
                    headers={"Authorization": f"token {access_token}"},
                )
                profile_json = api_request.json()
                username = profile_json.get("login")
                if username:
                    name = username
                    email = profile_json.get("email")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise githubException()
                        login(request, user)
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            email=email,
                            first_name=name,
                            login_method=models.User.LOGIN_GITHUB,
                            bio="",
                        )
                        user.set_unusable_password()
                        user.save()
                    print("이게 살아있어?", user)
                    login(request, user)
                    return redirect(reverse("core:home"))

                else:
                    raise githubException()
        else:
            raise githubException()
    except githubException:
        # 에러 메시지 보내기
        print("이미 존재하는 이메일입니다. 깃허브로 로그인 하지마세요")
        return redirect(reverse("users:login"))
