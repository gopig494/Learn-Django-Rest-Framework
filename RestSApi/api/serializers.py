from rest_framework import serializers
from RestSApi.models import *
from django.contrib.auth.models import User

class CityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["city"]

class CustomerModelSerializer(serializers.ModelSerializer):
    city = CityModelSerializer(read_only = True)
    country = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = "__all__"
        # fields = ["name"]
        # depth = 1
    
    def validate(self,request_data):
        if request_data.get("name"):
            special_characters = "@<([{\^-=$!|]})?*+.>"
            if any(x in special_characters for x in request_data.get("name")):
                raise serializers.ValidationError("Special characters are not allowed in the name.")
            # request_data["name"] = special_characters
            return request_data
    
    def validate_age(self,age):
        if age < 20:
            raise serializers.ValidationError("Age cannot be less than 20")
        return age
    
    def get_country(self,obj):
        return "india"

class CustomerSerializer(serializers.Serializer):
    name = serializers.EmailField()
    age = serializers.IntegerField()
    address = serializers.CharField()
    phone = serializers.CharField()

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate(self,rq_data):
        if rq_data.get("username"):
            exe_username = User.objects.filter(username = rq_data.get("username")).exists()
            if exe_username:
                raise serializers.ValidationError("Username already taken")  
        return rq_data
    
    def validate_email(self,email):
        if email:
            exe_username = User.objects.filter(email = email).exists()
            if exe_username:
                raise serializers.ValidationError("email already taken")  
        return email
    
    def create(self, validated_data):
        new_user = User.objects.create(first_name = validated_data.get("first_name"),last_name = validated_data.get("last_name"),
                                        email=validated_data.get("email"),username = validated_data.get("username"))
        new_user.set_password(validated_data.get("password"))
        new_user.save()
        return validated_data

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
