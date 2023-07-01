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

    """
       Get: Lists all passports with person 
    """
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
    
    class InputSerializer(serializers.ModelSerializer):
        passport_no = serializers.CharField(required=True)

        class Meta:
            model = Passport
            fields = ('passport_no', )

    """
        Post: Creates a Passport of a Person
    """
    def post(self, request):
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
        
        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(person=person)

        return Response({
            "success": True,
            "message": "Passport created successfully.",
            "data": serializer.data,
            "code": status.HTTP_201_CREATED,
        })
    
    """
        Update: Updates Passport details of a Person
    """
    def put(self, request):
        passport_id = request.query_params.get("id")
        person_id = request.query_params.get("person_id")

        person = Person.objects.filter(id=person_id).first()
        passport = Passport.objects.filter(id=passport_id).first()

        if not person:
            return Response(
                {
                    "success": False,
                    "message": "Person not found.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not passport:
            return Response(
                {
                    "success": False,
                    "message": "Passport not found.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # First check if the old person is same as the person (to be updated)
        old_person = passport.person
        if old_person != person:

            # Check if person already has a passport
            try: 
                if person.passport:
                    return Response(
                        {
                            "success": False,
                            "message": "Person already has a Passport.",
                            "code": status.HTTP_400_BAD_REQUEST,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Passport.DoesNotExist:
                return Response(
                        {
                            "success": False,
                            "message": f"Person with Id={person_id} doesnot have a Passport yet. First, create a Passport.",
                            "code": status.HTTP_400_BAD_REQUEST,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        serializer = self.InputSerializer(passport, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(person=person)

        return Response({
            "success": True,
            "message": "Passport details updated successfully.",
            "data": serializer.data,
            "code": status.HTTP_201_CREATED,
        })