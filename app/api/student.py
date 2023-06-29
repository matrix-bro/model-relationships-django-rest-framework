from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import Course, Student

class AllStudentView(APIView):
    class OutputSerializer(serializers.ModelSerializer):

        class CourseSerializer(serializers.ModelSerializer):
            class Meta:
                model = Course
                fields = ["id", "name", ]

        courses = CourseSerializer(many=True)

        class Meta:
            model = Student
            fields = ["id", "name", "courses"]

    def get(self, request):
        students_list = Student.objects.all()

        serializer = self.OutputSerializer(students_list, many=True)
        serialized_data = serializer.data

        return Response(
            {
                "success": True,
                "message": "All Students retrieved successfully.",
                "data": serialized_data,
                "code": status.HTTP_200_OK,
            }
        )