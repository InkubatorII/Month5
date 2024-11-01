from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def test_api_view(request):
    dict = {
        'str': 'Hello World'
    }
    return Response(data=dict, status=status.HTTP_200_OK)