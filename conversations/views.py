from users import models as user_models
from . import models, forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.views.generic import View
from django.http import Http404


def go_conversation(request, a_pk, b_pk):

    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    if user_one is not None and user_two is not None:
        try:
            conversation = (
                models.Conversation.objects.filter(participants=user_one)
                .filter(participants=user_two)
                .get()
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()

        # form = forms.AddCommentForm()

        return render(
            self.request,
            "conversations/conversation_detail.html",
            context={"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        if message is not None:
            conversation = models.Conversation.objects.get_or_none(pk=pk)
            if not conversation:
                raise Http404()
            models.Message.objects.create(
                user=self.request.user, conversation=conversation, message=message
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
