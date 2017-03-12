from images.models import Tokens, Images
from rest_framework import serializers

class TokensSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Tokens
		fields = ('token',)

class ImagesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Images
		fields = ('token' ,'filename', 'compression_percentage' )