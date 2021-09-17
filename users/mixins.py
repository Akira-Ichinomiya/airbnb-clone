from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect


class emailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "깃허브 또는 카카오를 통한 로그인은 접근이 불가능합니다.")
        return redirect("core:home")


class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "현재 로그인이 되어있습니다."

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):

        messages.error(self.request, self.permission_denied_message)
        return redirect("core:home")


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
