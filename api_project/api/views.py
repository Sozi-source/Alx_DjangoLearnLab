from django.shortcuts import render
from .models import Book
from rest_framework import generics, viewsets
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsOwner
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api import permissions
# Read-only for all, write for owners
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Use custom permission
    permission_classes = [IsOwnerOrReadOnly]
    
    # Optional: Filter queryset to show only user's books
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Book.objects.filter(user=user)
        return Book.objects.none()  # Or Book.objects.all() if you want public viewing
    
    def perform_create(self, serializer):
        # Automatically set the owner to the current user
        serializer.save(user=self.request.user)

# Different permission levels for different actions
class BookViewSetWithActionPermissions(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]  # Anyone can view
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]  # Only logged in can create
        else:  # update, partial_update, destroy
            permission_classes = [IsOwner]  # Only owners can modify
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })