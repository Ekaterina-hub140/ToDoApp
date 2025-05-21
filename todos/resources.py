from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Task, Category
from django.contrib.auth.models import User

class TaskResource(resources.ModelResource):
    # For foreign key relationships
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')  # Map by username
    )
    
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')  # Map by category name
    )
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'user', 'category', 'due_date', 'completed')
        export_order = fields  # Optional: set export column order
        skip_unchanged = True  # Skip unchanged records on import
        report_skipped = False  # Don't report skipped rows