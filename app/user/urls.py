from django.urls import path
from user.views import LoginView, cierreSesion, RegistroRev, ListaRevisores, ActualizacionRev

app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', cierreSesion, name="Logout"),
    path('RegistroRev/', RegistroRev.as_view(), name='Registro_Revisor'),
    path('listaRevisr/', ListaRevisores.as_view(), name='lista_revisor'),
    path('ActulizarRevisor/<slug:slug>', ActualizacionRev.as_view(), name='actualizar_Revisor'),
]

