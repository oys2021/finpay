from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "name", "accountType", "country",
                  "countryCode", "state", "address", "phoneNumber"]
        
    def create(self,validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        return {
            "status": 201,
            "message": "User registered successfully",
            "data": {
                "token": str(token.access_token),
                "user": {
                    "email": instance.email,
                    "name": instance.name,
                    "accountType": instance.accountType,
                    "country": instance.country,
                    "state": instance.state,
                }
            }
        }
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data.get("email"), password=data.get("password"))
        if not user:
            raise serializers.ValidationError({"message": "Invalid credentials"})
        token = RefreshToken.for_user(user)
        return {
            "status": 200,
            "message": "Login successfully",
            "data": {
                "token": str(token.access_token),
                "user": {
                    "email": user.email,
                    "name": user.name,
                    "accountType": user.accountType,
                }
            }
        }
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "User with this email does not exist"})

        user.set_password(data["password"])
        user.save()
        return {
            "status": 200,
            "message": "User password reset successfully",
            "data": {
                "email": user.email,
                "name": user.name,
                "accountType": user.accountType,
                "country": user.country,
                "state": user.state,
            }
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError({"message": "Token is invalid or expired"})

    
