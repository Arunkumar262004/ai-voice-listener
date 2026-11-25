from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Transcription
from .serializers import TranscriptionSerializer


@api_view(["GET"])
def health(request):
    return Response({"ok": True})


class TranscriptionViewSet(viewsets.ModelViewSet):
    """CRUD for transcription history.

    GET    /api/transcriptions?q=&skip=&limit=  -> {total, items}
    POST   /api/transcriptions
    GET    /api/transcriptions/{id}
    PUT    /api/transcriptions/{id}   (PATCH for partial)
    DELETE /api/transcriptions/{id}
    """

    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        q = request.query_params.get("q")
        if q:
            qs = qs.filter(text__icontains=q)
        try:
            skip = max(0, int(request.query_params.get("skip", 0)))
            limit = min(200, max(1, int(request.query_params.get("limit", 50))))
        except ValueError:
            skip, limit = 0, 50
        total = qs.count()
        items = self.get_serializer(qs[skip : skip + limit], many=True).data
        return Response({"total": total, "items": items})
