from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'calories', 'calorie_button')
    list_display_links = ('name',)
    search_fields = ['name']

    def calorie_button(self, obj):
        url = reverse('calorie_view', args=[obj.id])
        return format_html('<a href="{}" target="_blank">计算热量</a>', url)

    calorie_button.short_description = "卡路里计算"