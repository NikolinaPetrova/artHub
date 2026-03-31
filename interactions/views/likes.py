from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from artworks.models import Artwork
from groups.models import Post
from interactions.models import Like, Comment
from groups.utils import is_group_member
from notifications.services import NotificationService


class LikeView(LoginRequiredMixin, View):
    MODEL_MAP = {
        'artwork': Artwork,
        'post': Post,
        'comment': Comment,
    }

    def post(self, request, model_type, pk):
        model = self.MODEL_MAP.get(model_type)

        if not model:
            return redirect('home')

        obj = get_object_or_404(model, pk=pk)

        if model_type == 'post' and not is_group_member(request.user, obj.group):
            messages.error(request, 'You must be a group member to like posts.')
            return redirect('group-details', slug=obj.group.slug)

        if model_type == 'comment' and obj.post and not is_group_member(request.user, obj.post.group):
            messages.error(request, 'You must be a group member to like comments on posts.')
            return redirect('group-details', slug=obj.post.group.slug)

        like_data = {'user': request.user}

        if model_type == 'artwork':
            like_data['artwork'] = obj
        elif model_type == 'post':
            like_data['post'] = obj
        elif model_type == 'comment':
            like_data['comment'] = obj

        like, created = Like.objects.get_or_create(**like_data)
        if created:
            NotificationService.notify_like(obj, request.user)
        if not created:
            like.delete()

        return redirect(request.META.get('HTTP_REFERER'))