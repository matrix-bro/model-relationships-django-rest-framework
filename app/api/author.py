from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import Author, Book

class AllAuthorView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
                
        class BookSerializer(serializers.ModelSerializer):
            class Meta:
                model = Book
                fields = ['id', 'title',]

        books = BookSerializer(many=True)

        class Meta:
            model = Author
            fields = ['id', 'name', 'books', ]

    """
       Get: Lists all authors with books 
    """
    def get(self, request):
        authors = Author.objects.all()
        serializer = self.OutputSerializer(authors, many=True)
        serialized_data = serializer.data

        return Response(
            {
                "success": True,
                "message": "All Author retrieved successfully.",
                "data": serialized_data,
                "code": status.HTTP_200_OK,
            }
        )
    

    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(required=True)

        class Meta:
            model = Author
            fields = ("name",)

    """
        Post: Creates an Author
    """
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Author created successfully.",
                "data": serializer.data,
                "code": status.HTTP_200_OK,
            }
        )