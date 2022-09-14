from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'address', 'is_active', 'is_admin']
    list_display_links = ['id', 'email']
    list_editable = ['is_active']
    list_per_page = 10
    list_filter = ['is_active', 'is_admin']
    actions = ['make_active']

    @admin.action(description='선택된 유저를 active 상태로 변경')
    def make_active(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(request, '{}명의 유저를 active 상태로 변경'.format(updated_count))
