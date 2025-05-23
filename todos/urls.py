from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, CategoryListCreateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    
  
]