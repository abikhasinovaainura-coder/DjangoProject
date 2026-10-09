from django.contrib import admin
from .models import Category, Medicine, Order, OrderItem, ChatMessage

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'total_price', 'payment_type', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'payment_type', 'created_at')
    search_fields = ('full_name', 'phone', 'address')
    inlines = [OrderItemInline]

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name_kk', 'category', 'price', 'stock', 'age_limit')
    list_filter = ('category',)
    search_fields = ('name_kk', 'name_ru', 'name_en')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'message', 'is_from_admin', 'created_at')
    list_filter = ('is_from_admin', 'created_at')
    search_fields = ('message', 'full_name', 'phone')

admin.site.register(Category)