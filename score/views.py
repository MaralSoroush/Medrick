from .models import Score
from .serializers import CreateScoreSerializer, ScoreBoardSerialzier
from rest_framework import viewsets, response
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F
from game.mixins import LoggingMixin


class ScoreView(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = CreateScoreSerializer
    serializer_class_board = ScoreBoardSerialzier

    def get_queryset(self):
        return Score.objects.all().annotate(rank=Window(expression=RowNumber(), order_by=[-F('score')],)).order_by(
            '-score')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().values()
        query_list = list(queryset)
        player_id = self.request.query_params.get('playerid')
        records = self.serializer_class_board(
            query_list[0:100], many=True)
        try:
            if player_id:
                player_id = int(player_id)
                if Score.objects.filter(player_id=player_id).exists():
                    for query in query_list:
                        if int(player_id) == query['player_id']:
                            serialzier = self.serializer_class_board(query)

                            return response.Response({**serialzier.data, "records": records.data})
                return response.Response(status=404, data={"msg": "player with this id not found"})
            return response.Response({"records": records.data})
        except ValueError:
            return response.Response(status=400, data={"msg": "enter an integer for player id"})
