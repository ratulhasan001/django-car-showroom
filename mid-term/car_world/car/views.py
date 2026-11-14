from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from . import forms
from .models import Car


class DetailCarView(DetailView):
    model = Car
    pk_url_kwarg = 'id'
    template_name = 'car_details.html'

    def post(self, request, *args, **kwargs):
        # Comments are open to every visitor (name and email are part of the form).
        self.object = self.get_object()
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = self.object
            new_comment.save()
            messages.success(request, 'Thanks, your comment was posted.')
            # Redirect so refreshing the page does not post the comment twice.
            return redirect('car_details', id=self.object.id)
        context = self.get_context_data(comment_form=comment_form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if 'comment_form' not in context:
            initial = {}
            if user.is_authenticated:
                initial = {'name': user.get_full_name() or user.username, 'email': user.email}
            context['comment_form'] = forms.CommentForm(initial=initial)
        context['comments'] = self.object.comments.order_by('-created_on')
        context['already_bought'] = (
            user.is_authenticated and self.object.buyers.filter(pk=user.pk).exists()
        )
        return context


@login_required
@require_POST
def update_quantity(request, id):
    car = get_object_or_404(Car, pk=id)
    if car.buyers.filter(pk=request.user.pk).exists():
        messages.info(request, f'You already bought the {car.model}.')
    else:
        # Only decrement when there is stock left; the filter makes this safe
        # even if two people buy the last car at the same time.
        updated = Car.objects.filter(pk=car.pk, quantity__gt=0).update(quantity=F('quantity') - 1)
        if updated:
            car.buyers.add(request.user)
            messages.success(request, f'You bought the {car.model}. It is now listed on your profile.')
        else:
            messages.error(request, f'Sorry, the {car.model} is out of stock.')
    return redirect('car_details', id=car.id)
