from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from accountapp.models import HelloWorld2

# Create your views here.

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
    success_url = reverse_lazy('accountapp:helloworld2')
    template_name = 'accountapp/create.html'
    
