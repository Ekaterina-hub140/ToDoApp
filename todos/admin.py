from django.contrib import admin
from .models import Category, Task
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget
from django.contrib.auth.models import User

# First define the inline and resource classes
class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('title', 'due_date', 'completed')
    show_change_link = True

class TaskResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )
    due_date = fields.Field(widget=DateWidget('%Y-%m-%d'))

    class Meta:
        model = Task
        fields = ('id', 'title', 'user', 'category', 'due_date', 'completed', 'description')
        export_order = fields
        import_id_fields = ('id',)

    def validate_category(self, value):
        if not Category.objects.filter(name=value).exists():
            raise ValueError(f"Category '{value}' does not exist")

    def before_import_row(self, row, **kwargs):
        """Set current user for new tasks if not specified"""
        if 'user' not in row or not row['user']:
            row['user'] = kwargs.get('user').username

# Then register your models
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_count')
    inlines = [TaskInline]
    
    def task_count(self, obj):
        return obj.task_set.count()
    task_count.short_description = 'Number of Tasks'

@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
    resource_class = TaskResource
    list_display = ('title', 'user', 'category', 'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'category', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'
    ordering = ('-created_at',)
    actions = ['mark_completed', 'mark_incomplete']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def mark_completed(self, request, queryset):
        queryset.update(completed=True)
    mark_completed.short_description = "Mark selected tasks as completed"
    
    def mark_incomplete(self, request, queryset):
        queryset.update(completed=False)
    mark_incomplete.short_description = "Mark selected tasks as incomplete"

    def get_import_resource_kwargs(self, request, *args, **kwargs):
        return {'user': request.user}