from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
  ListView, 
  DetailView, 
  CreateView, 
  UpdateView,
  DeleteView
)
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from allauth.account.views import PasswordChangeView
from coplate.forms import ReviewForm
from coplate.models import Review

# Create your views here.

class IndexView(ListView):
  model = Review
  template_name = "coplate/index.html"
  context_object_name = "reviews"
  paginate_by = 4
  ordering = ["-dt_created"]

class ReviewDetailView(DetailView):
  model = Review
  template_name = 'coplate/review_detail.html'
  pk_url_kwarg = "review_id"

class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Review
  form_class = ReviewForm
  template_name = 'coplate/review_form.html'

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse('review-detail', kwargs={"review_id":self.object.id})

  def test_func(self,user):
    return EmailAddress.objects.filter(user=user, verified=True).exists()
      

class ReviewUpdateView(UpdateView):
  model = Review
  form_class = ReviewForm
  template_name = 'coplate/review_form.html'
  pk_url_kwarg = 'review_id'

  def get_success_url(self):
    return reverse('review-detail', kwargs={"review_id":self.object.id})

class ReviewDeleteView(DeleteView):
  model = Review
  template_name = 'coplate/review_confirm_delete.html'
  pk_url_kwarg = 'review_id'

  def get_success_url(self):
    return reverse('index')

class CustomPasswordChangeView(PasswordChangeView):
  def get_success_url(self):
    return reverse("index")
