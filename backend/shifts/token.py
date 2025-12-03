from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ADD EXTRA CLAIMS HERE
        token["username"] = user.username
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser

        # If user has employee_profile relationship
        if hasattr(user, "employee_profile"):
            token["employee_id"] = user.employee_profile.id
            token["employee_name"] = user.employee_profile.name

        return token
