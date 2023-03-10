from rest_framework import serializers
from app.models import Travel, Position, Address, TravelCollection, Tag
from .schedule import ScheduleSerializer
from .user import UserSerializer, AppUser
from .address import AddressSerializer
from app.utilities import permission
from .images import Image
from utilities import mixins


class TravelCollectionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = TravelCollection
        fields = ['id', 'owner', 'title', 'create_time']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']


class TravelBriefSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    cover = serializers.PrimaryKeyRelatedField(read_only=True)
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    position = AddressSerializer(required=False, allow_null=True)
    likes = serializers.SerializerMethodField('count_likes')
    comments = serializers.SerializerMethodField('count_comments')

    def count_likes(self, obj):
        return obj.likes.count()

    def count_comments(self, obj):
        return obj.comments.count()

    class Meta:
        model = Travel
        exclude = ['forbidden_reason']

class TravelListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = mixins.PrimaryKeyNestedField(
        serializer=UserSerializer)  # serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())
    cover = serializers.PrimaryKeyRelatedField(read_only=True)
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    position = AddressSerializer(required=False, allow_null=True)
    likes = serializers.SerializerMethodField('count_likes')
    comments = serializers.SerializerMethodField('count_comments')
    # collection = mixins.PrimaryKeyNestedField(serializer=TravelCollectionSerializer)
    tag = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Tag.objects.all())

    def count_likes(self, obj):
        return obj.likes.count()

    def count_comments(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        position = validated_data.get('position', None)
        if position is not None:
            validated_data['position'] = Address.objects.create(**position)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        position = validated_data.get('position', None)
        if position is not None:
            if instance.position:
                validated_data['position'], *_ = Address.objects.update_or_create(defaults=position,
                                                                                  id=instance.position_id)
            else:
                validated_data['position'] = Address.objects.create(**position)
        return super().update(instance, validated_data)

    class Meta:
        model = Travel
        exclude = ['forbidden_reason','collection']


class TravelSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = mixins.PrimaryKeyNestedField(
        serializer=UserSerializer)  # serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())
    cover = serializers.PrimaryKeyRelatedField(read_only=True)
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    position = AddressSerializer(required=False, allow_null=True)
    likes = serializers.SerializerMethodField('count_likes')
    comments = serializers.SerializerMethodField('count_comments')
    collection = mixins.PrimaryKeyNestedField(serializer=TravelCollectionSerializer)
    schedule = mixins.PrimaryKeyNestedField(required=False, serializer=ScheduleSerializer)
    tag = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Tag.objects.all())

    def count_likes(self, obj):
        return obj.likes.count()

    def count_comments(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        position = validated_data.get('position', None)
        if position is not None:
            validated_data['position'] = Address.objects.create(**position)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        position = validated_data.get('position', None)
        if position is not None:
            if instance.position:
                validated_data['position'], *_ = Address.objects.update_or_create(defaults=position,
                                                                                  id=instance.position_id)
            else:
                validated_data['position'] = Address.objects.create(**position)
        return super().update(instance, validated_data)

    class Meta:
        model = Travel
        exclude = ['forbidden_reason']


class TravelAddressSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    position = AddressSerializer(read_only=True)

    class Meta:
        model = Travel
        fields = ['id', 'position', 'time']


class TravelCollectionDetailedSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    collection_travels = TravelBriefSerializer(required=False, allow_null=True, many=True)
    open = serializers.ReadOnlyField(default=False, required=False)

    class Meta:
        model = TravelCollection
        fields = ['id', 'title', 'create_time', 'collection_travels', 'owner', 'open']
