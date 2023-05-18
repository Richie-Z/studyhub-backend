from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from project.helpers import create_response
from repository.models import Repository

from .forms import RepositoryForm


@permission_classes([IsAuthenticated])
class CreateRepositoryView(APIView):
    def post(self, request):
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repository = Repository.objects.create_repository(**request.POST)
            return create_response("Success Create Repository", status.HTTP_201_CREATED)
        else:
            return create_response(
                "Error Create Repository",
                status.HTTP_400_BAD_REQUEST,
                {"errors": form.errors},
            )
