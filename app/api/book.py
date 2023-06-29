from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import Author, Book

class AllBookView(APIView):
    class OutputSerializer(serializers.ModelSerializer):

        class AuthorSerializer(serializers.ModelSerializer):
            class Meta:
                model = Author
                fields = ['id', 'name',]

        author = AuthorSerializer()

        class Meta:
            model = Book
            fields = ['id', 'title', "author"]

    def get(self, request):
        books = Book.objects.all()
        serializer = self.OutputSerializer(books, many=True)
        serialized_data = serializer.data

        return Response(
            {
                "success": True,
                "message": "All Book retrieved successfully.",
                "data": serialized_data,
                "code": status.HTTP_200_OK,
            }
        )