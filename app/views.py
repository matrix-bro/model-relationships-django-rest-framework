from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import Passport, Person

class AllPersonView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        
        class PassportSerializer(serializers.ModelSerializer):
            class Meta:
                model = Passport
                fields = ['id', 'passport_no',]

        passport = PassportSerializer()
        
        class Meta:
            model = Person
            fields = ['id', 'name', 'passport', ]

    def get(self, request):
        person_list = Person.objects.all()
        serializer = self.OutputSerializer(person_list, many=True)
        serialized_data = serializer.data

        return Response(
            {
                "success": True,
                "message": "All Person retrieved successfully.",
                "data": serialized_data,
                "code": status.HTTP_200_OK,
            }
        )

class AllPassportView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Passport
            fields = ['id', 'passport_no', ]

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

        

            
