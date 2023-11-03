from rest_framework import serializers
from .models import Score


class CreateScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"

    def validate_score(self, value):
        """
        checks if score is between 0 and 100
        """
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                {"msg": "invalid_score", "data": value})
        return value


class ScoreBoardSerialzier(serializers.Serializer):
    player_id = serializers.IntegerField()
    score = serializers.IntegerField()
    rank = serializers.IntegerField()
