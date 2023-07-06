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

    """
       Get: Lists all courses with students
    """
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
    
    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(required=True)

        class Meta:
            model = Course
            fields = ("name",)

    """
        Post: Creates a Course
    """
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Course created successfully.",
                "data": serializer.data,
                "code": status.HTTP_200_OK,
            }
        )
    
    """
        Put: Update details of a Course
    """
    def put(self, request):
        pass

    """
        Delete: Deletes a Course
    """
    def delete(self, request):
        pass