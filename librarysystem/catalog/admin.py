from django.contrib import admin

from django.contrib.admin.models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action', 'content_type', 'user', 'action_time')
    def action(self, obj):
        return str(obj)
    
admin.site.register(LogEntry, LogEntryAdmin)

from .models import Author, Publisher, Book, BookInstance, Profile
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Publisher)
# admin.site.register(BookInstance)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'id_number', 'email')

admin.site.register(Profile, ProfileAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'publisher', 'callnumber')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


