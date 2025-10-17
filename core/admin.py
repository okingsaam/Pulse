from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profissional, Servico, Agendamento

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('role', 'phone')}),
    )

admin.site.register(Profissional)
admin.site.register(Servico)
admin.site.register(Agendamento)
