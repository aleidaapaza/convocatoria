from django.contrib import admin
# Register your models here.

from user.models import Persona,EncargadoMAE,ResponsableP,User,Revisor,SuperUser

class personaAdm(admin.ModelAdmin):
    fields = ('nombre', 'apellido', 'cargo', 'celular')
    # Campos que se mostrarán en la lista del admin
    list_display = ('nombre', 'apellido', 'cargo', 'celular')
    # Opcional: Permitir búsqueda
    search_fields = ('nombre', 'cargo')

class encargadoMAEAdm(admin.ModelAdmin):
    fields = ('persona', 'carnet', 'asignacion', 'correo')
    list_display = ('persona', 'carnet', 'asignacion', 'correo')
    search_fields = ('persona', 'correo',)

class ResponsablePAdm(admin.ModelAdmin):
    fields = ('persona', 'correo',)
    list_display = ('slug', '__str__',)

class RevisorAdm(admin.ModelAdmin):
    fields = ('persona', 'user',)
    list_display = ('slug', '__str__',)

class SuperUserAdm(admin.ModelAdmin):
    fields = ('persona', 'user',)
    list_display = ('slug', '__str__',)

admin.site.register(Persona, personaAdm)
admin.site.register(EncargadoMAE, encargadoMAEAdm)
admin.site.register(ResponsableP, ResponsablePAdm)
admin.site.register(Revisor, RevisorAdm)
admin.site.register(SuperUser, SuperUserAdm)

class UserAdm(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'is_municipio', 'is_revisor', 'is_superuser')
    search_fields = ('username',)

admin.site.register(User, UserAdm)