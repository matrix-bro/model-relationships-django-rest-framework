from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import Passport, Person

class AllPassportView(APIView):
    class OutputSerializer(serializers.ModelSerializer):

        class PersonSerializer(serializers.ModelSerializer):
            class Meta:
                model = Person
                fields = ['id', 'name',]

        person = PersonSerializer()
        
        class Meta:
            model = Passport
            fields = ['id', 'passport_no', 'person', ]

    def get(self, request):
        passports = Passport.objects.all()
        serializer = self.OutputSerializer(passports, many=True)
        serialized_data = serializer.data

        return Response(
            {
                "success": True,
                "message": "All Passports retrieved successfully.",
                "data": serialized_data,
                "code": status.HTTP_200_OK,
            }
        )