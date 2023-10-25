from django.urls import path
from . import views
# this file is within dj_app




urlpatterns = [
    path('', views.home, name = 'home'),   # Home page.
    path('ourstory', views.ourstory, name = 'ourstory'),   # about page.
    path('contact', views.contact, name = 'contact'),   # contact page.
    path('gate_info', views.gate_info, name = 'gate_info'),
    path('source', views.source, name = 'source'), #source page.
    path('gate_check', views.gate_check, name = 'gate_check'), #gate_check page.
    path('flight_lookup', views.flight_lookup, name = 'flight_lookup'), #flight_lookup page.
    path('weather', views.weather, name = 'weather'), #weather page. 
    path('guide', views.guide, name = 'guide'), #guide page. 
    path('report', views.report_an_issue, name = 'report'), #report page 
 

]

