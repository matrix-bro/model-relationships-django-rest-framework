from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import Course, Student

class AllCourseView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        
        class StudentSerializer(serializers.ModelSerializer):
            class Meta:
                model = Student
                fields = ["id", "name", ]
        
        students = StudentSerializer(many=True)

        class Meta:
            model = Course
            fields = ["id", "name", "students"]

    def get(self, request):
        courses_list = Course.objects.all()

        serializer = self.OutputSerializer(courses_list, many=True)
        serialized_data = serializer.data

        return Response(
            {
                "success": True,
                "message": "All Courses retrieved successfully.",
                "data": serialized_data,
                "code": status.HTTP_200_OK,
            }
        )