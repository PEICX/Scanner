from django.shortcuts import render, render_to_response
from django.views.generic.base import View

# Create your views here.



class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {
        })

class ScanView(View):
    def get(self, request):
        return render(request, 'scan.html', {
        })

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html', {
        })

class HelpView(View):
    def get(self, request):
        return render(request, 'help.html', {
        })


def page_not_found(request):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    # 全局500处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

def permission_denied(request):
    # 全局403处理函数
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response