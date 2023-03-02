from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):

    #write only ensures the field can only be written in but not read from. This is to ensure security
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = AppUser

        fields = ['email', 'username', 'firstname', 'lastname', 'password', 'password2']

        #make them all required
        extra_kwargs = {
            'firstname': {'required': True},
            'lastname': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
        }

    def create(self, validated_data):

        #after .pop(), validated_data doesn't contain the password property anymore, instead it's been moved to the password2 variable.
        password2 = validated_data.pop('password2')

        #I want to retain password because this argument needs to be passed in to create_user, which will run set_password(passed password) within it. 
        password = validated_data.get('password')

        if password == None or password2 == None:
            raise ValueError("No password entered!")

        if password != password2:
            raise ValueError("passwords do not match!")

        # the objects attribute is a manager object that is automatically created for every model. The objects attribute provides a set of methods that can be used to query the database for objects of the model.
        # create_user() method is not a built-in Django method, but rather a custom method that is defined in the AppUserManager class.
        appuser = AppUser.objects.create_user(**validated_data)
        # appuser.set_password(password)
        appuser.save()
        return appuser
   
