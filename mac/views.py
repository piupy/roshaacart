
from django.http import HttpResponse

from django.shortcuts import render


def index(request):
	return render(request,"mac/index.html")

