from django.contrib import admin
from .models import Post , Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #fields = (('title','slug'),'author') after click on blog it shows title and slug in one line and author in next line
    list_display = ('title','slug','author','publish','status') # how models should look
    list_filter = ('status','created','publish','author') #add filter to title and body
    prepopulated_fields = {'slug':('title',)} #generate slug field value automaticly from title field . also add more fields
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' #will include a date-based drilldown navigation by that field
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')