from .models import *
from rest_framework import serializers
from socialmedia import settings

class UserSerializer(serializers.ModelSerializer):
	"""
	Serilizer that returns the user details.
	"""
	class Meta:
		model = AppUser
		fields = "__all__"


class PostImageSerializer(serializers.ModelSerializer):
	"""
	Serializer that returns the image details
	"""
	class Meta:
		model = Image
		fields = "__all__"

class PostSerializer(serializers.HyperlinkedModelSerializer):
	"""
	Serializer that returns the post details
	"""
	images = serializers.SerializerMethodField()
	is_liked = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = ('id', 'subject', 'descripton', 'weight', 'images', 'is_liked')

	def create(self, validated_data):
		images_data = self.context.get('view').request.FILES
		post = Post.objects.create(**validated_data)
		for image_data in images_data.values():
			Image.objects.create(post=post, image=image_data)
		return post

	def get_images(self, obj):
		image_obj = Image.objects.filter(post=obj)
		image_list = []
		for each in image_obj:
			image_dict = {}
			image_dict.update({'image_url':"{0}{1}".format(settings.MEDIA_URL, each.image.url)})
			image_list.append(image_dict)
		return image_list

	def get_is_liked(self, obj):
		if obj.liked_users.filter(id=self.context['user'].id):
			return True
		return False
		
		

