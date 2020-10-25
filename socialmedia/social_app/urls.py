from django.urls import path,include
from social_app import views
from rest_framework import routers
from django.urls import include
router = routers.DefaultRouter()
router.register('app/users',views.UserViewSet)
"""
http://127.0.0.1:8000/posts/app/users/  #GET method, lists the whole users
http://127.0.0.1:8000/posts/app/users/  #POST method, creates the users
http://127.0.0.1:8000/posts/app/users/<int:pk>/  #PUT method, updates the users
http://127.0.0.1:8000/posts/app/users/<int:pk>/  #DELETE method, deletes the users
"""
router.register('app/admin/posts',views.PostViewset)
"""
http://127.0.0.1:8000/posts/app/admin/posts/  #GET method, lists the whole posts
http://127.0.0.1:8000/posts/app/admin/posts/  #POST method, creates the posts
http://127.0.0.1:8000/posts/app/admin/posts/<int:pk>/  #PUT method, updates the posts
http://127.0.0.1:8000/posts/app/admin/posts/<int:pk>/  #DELETE method, deletes the posts
"""

urlpatterns = [
	path('',include(router.urls)),
	path('api/user/posts/', views.UserActionViewset.as_view({"get":"get_user_posts"}), name='user_posts'),
	path('api/user/posts/<int:pk>/', views.UserActionViewset.as_view({"put":"user_response_to_post"}), name='user_posts_response'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]