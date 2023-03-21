from rest_framework import viewsets
from rest_framework.decorators import action
from NHL_Database import Data_Parser, models
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from NHL_Database import tasks
import logging

logger = logging.getLogger(__name__)

class ScrapingViewset(viewsets.GenericViewSet):
	def get_serializer_class(self):
		return serializers.Serializer

	@action(detail=False, methods=['post', 'get'])
	def init_db(self, request):
		"""
		Initializes database by getting starting data. Since this operation takes very long time and causes reset of
		entire database, confirmation parameter is required in body of request so that the accidental wipeout of
		database is prevented.
		This API should be used only when the database is being created anew, otherwise updates are preferable.
		:param request:
		:return:
		"""
		if request.method == 'GET':
			return Response(data=None, status=status.HTTP_200_OK)
		if request.data.get('contains', None):
			tables = ([cls.__name__ for cls in models.__subclasses__()])
			for table in tables:
				model = getattr(models, table)
				model.objects.all().delete()
				class_ = f'{table}Parser'
				parser_class = getattr(Data_Parser, class_)
				parser = parser_class()
				parser.process_data()
				return Response(status=status.HTTP_200_OK)
		return Response(data="abc", status=status.HTTP_200_OK)

	@action(detail=False, methods=['post', 'get'])
	def parse_table(self, request):
		"""
		Parses entire table. This also deletes all data from table if it existed previously.
		Data example: {"table": "Seasons"}
		:param request:
		:return:
		"""
		if request.method == 'GET':
			return Response(status=status.HTTP_200_OK)
		tasks.parse_table.delay(request.data)
		# data = request.data
		# table = data['table']
		# model = getattr(models, table)
		# model.objects.all().delete()
		# class_ = f'{table}Parser'
		# parser_class = getattr(Data_Parser, class_)
		# parser = parser_class()
		# parser.process_data()

		return Response(status=status.HTTP_200_OK)

	@action(detail=False, methods=['post'])
	def update_records(self, request):
		"""
		Removes records from database and replace them with updated version.
		{"table": "SkaterSeasonStats",
		"season": "20192020"}
		:param request:
		:return:
		"""
		if request.method == 'GET':
			return Response(status=status.HTTP_200_OK)
		data = request.data
		table = data['table']
		class_ = f'{table}Parser'
		parser_class = getattr(Data_Parser, class_)
		parser = parser_class()
		parser.update_data(**data)
		return Response(status=status.HTTP_200_OK)


	@action(detail=False)
	def add_records(self, request):
		"""
		Add new records to table based on params.
		:param request:
		:return:
		"""
		pass

	@action(detail=False)
	def remove_records(self, request):
		"""
		Remove records from database based on params.
		:param request:
		:return:
		"""
		pass
