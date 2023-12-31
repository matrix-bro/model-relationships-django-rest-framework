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

    """
       Get: Lists all person with passports 
    """
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
    
    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(required=True)

        class Meta:
            model = Person
            fields = ('name', )

    """
        Post: Creates a Person
    """
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            "success": True,
            "message": "Person created successfully.",
            "data": serializer.data,
            "code": status.HTTP_201_CREATED,
        })
    
    """
        Put: Update details of a Person
    """
    def put(self, request):
        person_id = request.query_params.get("id")
        person = Person.objects.filter(id=person_id).first()

        if not person:
            return Response(
                {
                    "success": False,
                    "message": "Person not found.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = self.InputSerializer(person, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Person Updated Successfully.",
                "data": serializer.data,
                "code": status.HTTP_200_OK,
            }
        )


    """
        Delete: Deletes a Person
    """
    def delete(self, request):
        person_id = request.query_params.get("id")

        person = Person.objects.filter(id=person_id).first()

        if not person:
            return Response(
                {
                    "success": False,
                    "message": "Person not found.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )    

        person.delete()

        return Response(
            {
                "success": True,
                "message": "Person deleted Successfully.",
                "code": status.HTTP_200_OK,
            }
        )


