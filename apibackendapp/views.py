from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee,Department
from .serializers import EmployeeSerializer, DepartmentSerializer, UserSerializer,SignupSerializer,LoginSerializer
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


# Create your views here.
class SignupAPIView(APIView):
     permission_classes = [AllowAny]
     def post(self,request):
          serializer = SignupSerializer(data = request.data)
          if serializer.is_valid():
               user = serializer.save()
               token,created = Token.objects.get_or_create(user=user)
               return Response({
                    "user_id":user.id,
                    "username": user.username,
                    "token" : token.key,
                    "role" : user.groups.all()[0].id if user.groups.exists() else None
               },status=status.HTTP_201_CREATED)
          else:
               response={'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}     
               return Response(response,status=status.HTTP_400_BAD_REQUEST)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Initialize the serializer with the data from the request
        serializer = LoginSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Extract the username and password from the validated data
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            # Check if authentication was successful
            if user is not None:
                # Retrieve the token for the authenticated user
                token = Token.objects.get(user=user)
                
                # Prepare the response data
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "username": user.username,
                    "role": user.groups.all()[0].id if user.groups.exists() else None,
                    "date": {
                        "token": token.key
                    }
                }
                # Return the response with status 200 OK
                return Response(response, status=status.HTTP_200_OK)  # Login is successful
                
            else:
                # If authentication fails
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid username or password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)  # Login failed
        
        else:
            # If the serializer is not valid
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'data': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

#Create viewset class inheriting the ModelViewSet class
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all() #Get all objects of the Model
    serializer_class = DepartmentSerializer #And render it using this serializer
    permission_classes= [IsAuthenticated] #to bipass the authentication

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all() #Get all objects of the Model
    serializer_class = EmployeeSerializer #And render it using this serializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['EmployeeName','Designation']
    # permission_classes= [IsAuthenticated]
    permission_classes= []

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() #Get all objects of the Model
    serializer_class = UserSerializer #And render it using this serializer
    permission_classes= [IsAuthenticated]
