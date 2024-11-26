"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from proyecto.view.itcp4 import descargar_archivo
from proyecto.view.itcp5 import descargar_archivo_der
from proyecto.view.itcp11 import descargar_docDeclaracion

urlpatterns = [
    path('',include('convocatoria.urls')),
    path('solicitud/',include('solicitud.urls')),
    path('admin/', admin.site.urls),
    path('userl/',include('user.urls')),
    path('proyecto/',include('proyecto.urls')),
    path('descargar_modelo_acta/<slug:slug>/<int:id>', descargar_archivo, name='descargar_modeloacta'),
    path('descargar_derecho_prop/<slug:slug>/<int:id>', descargar_archivo_der, name='descargar_derechoProp'),
    path('descargar_dclaracion/<slug:slug>/<int:num>', descargar_docDeclaracion, name='descargar_docDeclaracion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

