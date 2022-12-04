from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from accountapp.decorators import account_ownership_required

from accountapp.models import HelloWorld2
from accountapp.templates.accountapp.forms import AccountUpdateForm

# Create your views here.



has_ownership = [account_ownership_required, login_required]



def hello_world2(request):
    if request.method == "POST":
        temp = request.POST.get('hello_world_input')
        
        new_hello_world = HelloWorld2()
        new_hello_world.text = temp
        new_hello_world.save()
        
        return HttpResponseRedirect(reverse('accountapp:helloworld2'))
    else:
        hello_world_list = HelloWorld2.objects.all()
        return render(request, 'accountapp/hello_world2.html', context={'hello_world_list': hello_world_list})
    
    
class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('rankstatapp:summoners')
    template_name = 'accountapp/create.html'
    

class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

@method_decorator(has_ownership,'get')
@method_decorator(has_ownership,'post')

class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('rankstatapp:summoners')
    template_name = 'accountapp/update.html'

@method_decorator(has_ownership,'get')
@method_decorator(has_ownership,'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'