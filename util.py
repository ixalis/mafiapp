from django.shortcuts import render

def message(request, m):
	return render(request, 'userinterface/message.html', {'message': m})