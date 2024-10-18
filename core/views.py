from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator



# @method_decorator(ratelimit(key='ip', rate='3/m', block=True), name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

   

@login_required
def home_view(request):
  return render(request, 'home.html')