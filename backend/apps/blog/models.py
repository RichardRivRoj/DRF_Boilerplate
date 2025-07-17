import uuid

from django.db import models
from django.utils.text import slugify

def blog_thumbnail_directory(instance, filename):
    return "blog/{0}/{1}".format(instance.title, filename)

def category_thumbnail_directory(instance, filename):
    return "blog_categories/{0}/{1}".format(instance.name, filename)


class Category(models.Model):
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    
    name = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to=category_thumbnail_directory, blank=True, null=True)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)

class Post(models.Model):
    
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
    
    status_options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=blog_thumbnail_directory, blank=True, null=True)
    
    keywords = models.CharField(max_length=128, blank=True)
    slug = models.SlugField(max_length=128, unique=True)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=status_options, default='draft')
    
    objects = models.Manager()  # Default manager
    post_objects = PostObjects()  # Custom manager for published posts

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ("status", "-created_at")  # Order by status and then by creation date
        
class Heading(models.Model):
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='headings')
    
    text = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)
    level = models.PositiveIntegerField(
        choices=(
            (1, 'H1'),
            (2, 'H2'),
            (3, 'H3'),
            (4, 'H4'),
            (5, 'H5'),
            (6, 'H6'),
        )
    )  # 1 for H1, 2 for H2, etc.
    order = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.text} (Level {self.level})"
    
    class Meta:
        verbose_name = 'Heading'
        verbose_name_plural = 'Headings'
        ordering = ['order']  
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        super().save(*args, **kwargs)
