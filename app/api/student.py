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
        # Request comes with student name and old course id (optional) which is to be updated
        # If request also comes with old course id then we need to provide new course id (required)
        # Can update only student name
        # Can update student name with course (change course)

        student_id = request.query_params.get("id")
        old_course_id = request.query_params.get("old_course_id")
        student = Student.objects.filter(id=student_id).first()

        if not student:
            return Response(
                {
                    "success": False,
                    "message": "Student not found.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if old_course_id:
            # If old_course_id is given, we want course_id (new) to be required field.
            course_id = request.data.get("course_id")
            if not course_id:
                return Response(
                        {
                            "success": False,
                            "message": "course_id is required.",
                            "code": status.HTTP_400_BAD_REQUEST,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            old_course = Course.objects.filter(id=old_course_id).first()

            if not old_course:
                return Response(
                    {
                        "success": False,
                        "message": "Course not found.",
                        "code": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            student_courses = student.courses.all()
            if not old_course in student_courses:
                return Response(
                    {
                        "success": False,
                        "message": "Student is not enrolled in this Course.",
                        "code": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if course_id:
                course = Course.objects.filter(id=course_id).first()
                if not course:
                    return Response(
                        {
                            "success": False,
                            "message": "Course not found.",
                            "code": status.HTTP_400_BAD_REQUEST,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
                if course in student_courses:
                    return Response(
                    {
                        "success": False,
                        "message": "Student is already enrolled in this Course.",
                        "code": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.InputSerializer(student, data=request.data)

        serializer.is_valid(raise_exception=True)
        
        student.name = serializer.validated_data['name']
        student.save()

        
        if old_course_id:
            course_student = CourseStudent.objects.filter(student=student, course=old_course).first()

            course_student.course = course
            course_student.student = student
            course_student.date_enrolled = timezone.now()
            course_student.save()

        return Response(
            {
                "success": True,
                "message": "Student details updated successfully.",
                "data": serializer.data,
                "code": status.HTTP_200_OK,
            }
        )

    """
        Delete: Deletes a Student
    """
    def delete(self, request):
        pass