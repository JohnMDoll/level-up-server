"""View module for handling requests about game types"""
from django.db.models import Q
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer
from rest_framework.decorators import action


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event type
        """
        try:
            event = Event.objects.annotate(
                attendees_count=Count('attendees')).get(pk=pk)

            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # events = Event.objects.all()
        events = Event.objects.annotate(
            attendees_count=Count('attendees'),
            joined=Count('attendees', filter=Q(attendees=gamer))
        )

        # Set the `joined` property on every event
        # for event in events:
        #     # Check to see if the gamer is in the attendees list on the event
        #     event.joined = gamer in event.attendees.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized event instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        # pre-validation code
        # game = Game.objects.get(pk=request.data["game"])
        # event = Event.objects.create(
        #     date=request.data["date"],
        #     description=request.data["description"],
        #     game=game,
        #     organizer=gamer,
        # )
        # validation code
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(name=request.data["game"]["name"])
        gamer = Gamer.objects.get(user=request.auth.user)

        event = Event.objects.get(pk=pk)
        event.date = request.data["date"]
        event.description = request.data["description"]
        event.game = game
        event.organizer = gamer
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event

        Returns:
            Response -- {'message': 'Gamer added'},  with 201 status code
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to un-signup for an event

        Returns:
            Response -- {'message': 'Gamer removed'},  with 201 status code
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['description', 'date', 'game']


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for event
    """
    attendees_count = serializers.IntegerField(default=None)

    class Meta:
        model = Event
        fields = ('id', 'date', 'description', 'game', 'organizer',
                  'attendees', 'joined', 'attendees_count')
        depth = 2
