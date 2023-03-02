from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

# Create your views here.

#class for registering users
class Register(APIView):

    def post(self, request, format='json'):
        #this register_serializer is NOT built in, its a variable defined by myself, unlike the serializer_class used in GenericAPIView. This is APIView, so serializer_class is not applicable, this needs to be done differently.
        register_serializer = RegisterSerializer(data=request.data)

        # If the data passes all of the validation checks, is_valid() will return True. If any validation errors are encountered, is_valid() will return False. 
        if register_serializer.is_valid():
            register_serializer.save()

            #response as per django rest framework documentation: https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
            return Response(register_serializer.data, status=status.HTTP_201_CREATED)

        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


