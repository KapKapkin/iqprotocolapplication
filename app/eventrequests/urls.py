from django.urls import path
from eventrequests import views
urlpatterns = [
    path('', views.create_event, name='event_form'),
    path('window/delete/<int:pk>/', views.delete_window, name='window_delete'),
    path('event/<int:pk>/', views.show_event, name='event')
]
