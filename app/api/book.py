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

    """
       Get: Lists all books with authors 
    """
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
    
    class InputSerializer(serializers.ModelSerializer):
        title = serializers.CharField(required=True)

        class Meta:
            model = Book
            fields = ("title", )

    """
        Post: Creates a Book
    """
    def post(self, request):
        author_id = request.query_params.get("id")
        author = Author.objects.filter(id=author_id).first()

        if not author:
            return Response(
                {
                    "success": False,
                    "message": "Author doesnot exist.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.InputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        
        serializer.save(author=author)

        return Response(
            {
                "success": True,
                "message": "Book Created Successfully.",
                "data": serializer.data,
                "code": status.HTTP_200_OK,
            }
        )
    
    """
        Put: Update details of a Book
    """
    def put(self, request):
        author_id = request.query_params.get("author_id")
        book = Book.objects.filter(id=request.query_params.get("id")).first()

        if not book:
            return Response(
                {
                    "success": False,
                    "message": "Book not found.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if author_id:
            author = Author.objects.filter(id=request.query_params.get("author_id")).first()
            if not author:
                return Response(
                    {
                        "success": False,
                        "message": "Author not found.",
                        "code": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            book.author = author
        
        serializer = self.InputSerializer(book, data=request.data)

        serializer.is_valid(raise_exception=True)
        
        book.title = serializer.validated_data['title']
        book.save()

        return Response(
            {
                "success": True,
                "message": "Book details updated successfully.",
                "data": serializer.data,
                "code": status.HTTP_200_OK,
            }
        )


    """
        Delete: Deletes a Book
    """
    def delete(self, request):
        book_id = request.query_params.get("id")

        book = Book.objects.filter(id=book_id).first()

        if not book:
            return Response(
                {
                    "success": False,
                    "message": "Book not found.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )    

        book.delete()

        return Response(
            {
                "success": True,
                "message": "Book deleted successfully.",
                "code": status.HTTP_200_OK,
            }
        )