from django.contrib import admin
from .models import DiscussionBoard, Message
# Register your models here.


admin.site.register(DiscussionBoard)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'discussion_board', 'content', 'created_at', 'is_edited')
    list_filter = ('discussion_board', 'author', 'is_edited', 'created_at')
    search_fields = ('content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)