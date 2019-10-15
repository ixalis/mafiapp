from django.shortcuts import render
from engine.models import *
from django.contrib.auth.decorators import login_required

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'userinterface/signup.html', {'form': form})

@login_required
def profile(request):
	return render(request, 'registration/profile.html')

@login_required
def home(request):
	players = Player.objects.filter(user__username=request.user.username)
	gms = GM.objects.filter(user__username=request.user.username)
	context = {'players': players, 'gms': gms}
	return render(request, 'userinterface/home.html', context)