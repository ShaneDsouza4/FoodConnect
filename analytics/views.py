from django.shortcuts import render

# Create your views here.
def analytics_view(request):
    return render(request, 'webpages/analytics.html')