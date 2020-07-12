from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.validators import UniqueValidator
from accounts.models import User
from decks.models import Operator, Cluster
from decks.serializers import DeckSerializer, OperatorSerializer
from inspections.models import Inspection
from inspections.serializers import InspectionStatusSerializer, InspectionTypeNoSchemaSerializer


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class GroupsSerializer(serializers.ModelSerializer):
    permissions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = GroupsSerializer
    operator = OperatorSerializer
    clusters = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Cluster.objects.all()
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    alias = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        groups = validated_data.get('groups')
        clusters = validated_data.get('clusters')

        validated_data.pop('groups')
        validated_data.pop('clusters')

        user = self.Meta.model.objects.create_user(
            **validated_data
        )

        password = validated_data.get('password')
        if password:
            user.set_password(password)

        [user.groups.add(group) for group in groups]
        [user.clusters.add(cluster) for cluster in clusters]

        return user

    class Meta:
        model = User
        exclude = ('user_permissions', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active')


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("email", "password")


class UserInspectionSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    user_assigned = UserSerializer()
    scheduled_by = UserSerializer()
    completed_by = UserSerializer()
    status = InspectionStatusSerializer()
    type = InspectionTypeNoSchemaSerializer()
    deck = DeckSerializer()

    class Meta:
        model = Inspection
        exclude = ('updated',)
        depth = 1
