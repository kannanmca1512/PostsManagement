from .models import AppUser
from rest_framework import viewsets
from rest_framework import permissions, status
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited or delete.
    """
    permission_classes = [IsAuthenticated]
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer

class PostViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited or delete.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class UserActionViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or like and dislike by users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def __avg_user_interested_post_weight(self, post_objects):
        """
        Used to find the user interested posts contents
        """
        total_posts = post_objects.count()
        post_weight = 0
        for each in post_objects:
            post_weight += each.weight
        average_post_weight = post_weight // total_posts
        return average_post_weight

    def __user_interested_post_filter(self, avg_user_liked_post_weight):
        """
        Helps to find the user interested posts
        """
        query = Post.objects.extra(select={'is_top': "weight = " + str(avg_user_liked_post_weight)})
        resultant_obj = query.extra(order_by = ['-is_top'])
        return resultant_obj

    def get_user_posts(self, request):
        """
        Lists the posts based on the user's interest 
        """
        post_objects = Post.objects.filter(liked_users__id=request.user.id)
        avg_user_liked_post_weight = self.__avg_user_interested_post_weight(post_objects)
        queryset = self.__user_interested_post_filter(avg_user_liked_post_weight)
        context = {'user':request.user}
        serializer = PostSerializer(queryset, many=True, context=context)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def user_response_to_post(self, request, pk):
        """
        Likes if the user is not like the post, and vice versa
        """
        post_objects_count = Post.objects.filter(id=pk, liked_users__id=request.user.id).count()
        post_objects = Post.objects.get(id=pk)
        if post_objects_count !=0:
            post_objects.liked_users.remove(request.user)
            response_msg = "You disliked the post"
        else:
            post_objects.liked_users.add(request.user)
            response_msg = "You have liked the post"
        return Response({'data': response_msg}, status=status.HTTP_200_OK)
        



