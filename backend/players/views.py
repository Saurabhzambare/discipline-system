from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PlayerSerializer, PlayerPathUpdateSerializer


class PlayerMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PlayerSerializer(request.user.player)
        return Response(serializer.data)


class PlayerPathView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = PlayerPathUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        player = request.user.player
        player.path = serializer.validated_data["path"]
        player.save(update_fields=["path", "updated_at"])

        return Response(PlayerSerializer(player).data)
