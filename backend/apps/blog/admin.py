from django.contrib import admin
from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Post, Category, Heading, PostAnalytics

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'parent', 'slug')
    search_fields = ('name', 'title', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
    ordering = ('name',)
    readonly_fields = ('id',)
    list_editable = ('title',)
    
class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1
    fields = ('text', 'level', 'order', 'slug')
    prepopulated_fields = {'slug': ('text',)}
    ordering = ('order',)
    
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    
    list_display = ('title', 'category', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'content', 'keywords', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'slug', 'description', 'content', 'thumbnail', 'keywords', 'category')
        }),
        ('Status & Dates', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    inlines = [HeadingInline]
    
#@admin.register(Heading)
#class HeadingAdmin(admin.ModelAdmin):
#    list_display = ('text', 'post', 'level', 'order')
#    search_fields = ('text', 'post__text')
#    list_filter = ('level', 'post')
#    ordering = ('post', 'order')
#    prepopulated_fields = {'slug': ('text',)}


@admin.register(PostAnalytics)
class PostAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'views', 'impressions', 'clicks', 'click_through_rate', 'avg_time_on_page')
    search_fields = ('post__title',)
    readonly_fields = ('post','views', 'impressions', 'clicks', 'click_through_rate', 'avg_time_on_page')
    
    def post_title(self, obj):
        return obj.post.title
    
    post_title.short_description = 'Post Title'