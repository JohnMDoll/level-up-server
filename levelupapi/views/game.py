"""View module for handling requests about game types"""
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Count
from levelupapi.models import Game, Gamer, GameType, Event

class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.annotate(
            event_count=Count('game_events'),
            user_event_count=Count('game_events', filter=Q(game_events__organizer__user=request.user))
            ).get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.annotate(
            event_count=Count('game_events'),
            user_event_count=Count('game_events', filter=Q(game_events__organizer__user=request.user))
            )
        print(games.query)

        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        # Pre- post validation function script except return
        # gamer = Gamer.objects.get(user=request.auth.user)
        # game_type = GameType.objects.get(pk=request.data["game_type"])

        # game = Game.objects.create(
        #     name=request.data["name"],
        #     maker=request.data["maker"],
        #     number_of_players=request.data["number_of_players"],
        #     skill_level=request.data["skill_level"],
        #     gamer=gamer,
        #     game_type=game_type
        # )
        # serializer = GameSerializer(game)

        # new code to validate post requests, uses new CreateGameSerializer

        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.name = request.data["name"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["game_type"]['id'])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [ 'name', 'maker', 'number_of_players', 'skill_level', 'game_type']

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game
    """
    event_count = serializers.IntegerField(default=None)
    user_event_count = serializers.IntegerField(default=None)

    class Meta:
        model = Game
        fields = ('id', 'name', 'game_type', 'gamer', 'number_of_players', 'skill_level', 'maker', 'event_count', 'user_event_count')
        depth = 1