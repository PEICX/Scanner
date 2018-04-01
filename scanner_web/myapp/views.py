from django.shortcuts import render, render_to_response
from django.views.generic.base import View
from django.http import HttpResponse

# Create your views here.

class DoForm(View):

    def get(self, request):
        pass

    def post(self, request):
        return HttpResponse("sucess")

class Form(View):

    def get(self, request):
        return render(request, "test.html", {})

    def post(self, request):
        return HttpResponse("sucess")