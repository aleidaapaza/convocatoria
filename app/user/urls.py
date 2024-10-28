from django.urls import path
from user.views import LoginView, cierreSesion, RegistroRev

app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', cierreSesion, name="Logout"),
    path('RegistroRev', RegistroRev.as_view(), name='Registro_Revisor'),
]

