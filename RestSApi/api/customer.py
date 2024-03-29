from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from RestSApi.models import Customer
from RestSApi.api.serializers import * 
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(["GET","POST","PUT","DELETE","PATCH"])
def get_info(request):
    if request.method == "GET":
        if request.GET.get("name"):
            cust_query_set = Customer.objects.get(name = request.GET.get("name"))
            cust_serializer = CustomerModelSerializer(cust_query_set)
        else:
            cust_query_set = Customer.objects.all()
            cust_serializer = CustomerModelSerializer(cust_query_set, many=True)
        return Response({"status":"success","data":cust_serializer.data},status = status.HTTP_200_OK)
    elif request.method == "POST":
        cust_serializer = CustomerSerializer(data = request.data)
        if cust_serializer.is_valid():
            cust_serializer.save()
            return Response({'status': "success","message":cust_serializer.data},status = status.HTTP_201_CREATED)
        else:
            return Response({'status': "failed","message":cust_serializer.errors},status = status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT" or request.method == "PATCH":
        exe_obj = Customer.objects.get(id=request.data.get('id'))
        if exe_obj:
            if request.method == "PUT":
                cust_serializer = CustomerModelSerializer(exe_obj,data = request.data)
            else:
                cust_serializer = CustomerModelSerializer(exe_obj,data = request.data, partial = True)
            if cust_serializer.is_valid():
                cust_serializer.save()
                return Response({'status': "success","message":cust_serializer.data},status = status.HTTP_201_CREATED)
            else:
                return Response({'status': "failed","message":cust_serializer.errors},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': "failed","message":"No such customer exists"},status = status.HTTP_404_NOT_FOUND)

class CustomerCrud(APIView):
    def get(self,request):
        query = Customer.objects.get(id=request.GET.get('id'))
        serialize = CustomerModelSerializer(query)
        return Response({"status":"success","data":serialize.data},status = status.HTTP_200_OK)
    
    def post(self,request):
        serializer = CustomerModelSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': "success","message":serializer.data},status = status.HTTP_201_CREATED)
        else:
            return Response({'status': "failed","message":serializer.errors},status = status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        exe_obj = Customer.objects.get(id=request.data.get('id'))
        if exe_obj:
            serializer = CustomerModelSerializer(exe_obj,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': "success","message":serializer.data},status = status.HTTP_201_CREATED)
            else:
                return Response({'status': "failed","message":serializer.errors},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': "failed","message":"No such customer exists"},status = status.HTTP_404_NOT_FOUND)
    
    def patch(self,request):
        exe_obj = Customer.objects.get(id=request.data.get('id'))
        if exe_obj:
            serializer = CustomerModelSerializer(exe_obj,data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': "success","message":serializer.data},status = status.HTTP_201_CREATED)
            else:
                return Response({'status': "failed","message":serializer.errors},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': "failed","message":"No such customer exists"},status = status.HTTP_404_NOT_FOUND)
    
    def delete(self,request):
        exe_obj = Customer.objects.get(id = request.data.get('id'))
        if exe_obj:
            exe_obj.delete()
            return Response({'status': "success"},status = status.HTTP_201_CREATED)
        else:
            return Response({'status': "failed","message":"No such customer exists"},status = status.HTTP_404_NOT_FOUND)

class CustomerViewset(viewsets.ModelViewSet):
    serializer_class = CustomerModelSerializer
    queryset = Customer.objects.all()

    def list(self, request):
        if request.GET.get('id'):
            cust_queryset = Customer.objects.get(id = request.GET.get('id'))
            serializer = CustomerModelSerializer(cust_queryset).data
        elif request.GET.get('search_data'):
            cust_queryset = Customer.objects.filter( name__startswith = request.GET.get('search_data'))
            serializer = CustomerModelSerializer(cust_queryset, many = True).data
        else:
            cust_queryset = Customer.objects.all()
            serializer = CustomerModelSerializer(cust_queryset, many = True).data
            # serializer = []
        return Response({'status': "success","data":serializer},status=status.HTTP_200_OK)
    
@api_view(["POST"])
def register_user(request):
    from RestSApi.api.serializers import UserSerializer
    serializer_resp = UserSerializer(data = request.data)
    if serializer_resp.is_valid():
        serializer_resp.save()
        return Response({'status': "success","message":serializer_resp.data},status = status.HTTP_201_CREATED)
    else:
        return Response({"status":"failed","message":serializer_resp.errors},status = status.HTTP_400_BAD_REQUEST)

class UserCrud(APIView):
    def post(self,request):
        seri_resp = UserLoginSerializer(data = request.data)
        if seri_resp.is_valid():
            user = authenticate(username = request.data.get("username"),password = request.data.get("password"))
            if user:
                resp = {}
                resp.update(UserSerializer(user).data)
                token = Token.objects.get_or_create(user = user)
                resp["token"] = str(token[0])
                return Response({"status":"success","message":resp},status = status.HTTP_200_OK)
            else:
                return Response({"status":"failed","message":"Invalid username or password"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":"failed","message":seri_resp.errors},status = status.HTTP_400_BAD_REQUEST)