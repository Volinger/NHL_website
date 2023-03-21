from rest_framework import serializers
from NHL_Database import models


class SeasonsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Seasons
		fields = '__all__'
