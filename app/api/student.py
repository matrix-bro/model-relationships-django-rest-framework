from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from app.models import Course, CourseStudent, Student

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

    """
       Get: Lists all students with courses
    """
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
    
    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(required=True)

        class Meta:
            model = Student
            fields = ("name", )
    
    """
        Post: Creates a Student
    """
    def post(self, request):
        course_id = request.query_params.get("id")
        course = Course.objects.filter(id=course_id).first()

        if not course:
            return Response(
                {
                    "success": False,
                    "message": "Course doesnot exist.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        student = serializer.save()

        CourseStudent.objects.create(course=course, student=student, date_enrolled=timezone.now())

        return Response(
            {
                "success": True,
                "message": "Student created successfully.",
                "data": serializer.data,
                "code": status.HTTP_200_OK,
            }
        )
    
    """
        Put: Update details of a Student
    """
    def put(self, request):
        pass

    """
        Delete: Deletes a Student
    """
    def delete(self, request):
        pass