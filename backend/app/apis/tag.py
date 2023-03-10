import random
from math import floor

from django.db.models import Count, Q
from jieba import xrange
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from app.response import *

from utilities import conversion, permission as _permission, filters
from django_filters.rest_framework import DjangoFilterBackend
from app.utilities import permission
from app.models import Travel, AppUser, Image, Address, Comment, Message, TravelCollection, Tag
from app.serializers import TagSerializer


class TagFilterBackend(filters.QueryFilterBackend):

    def filter_queryset(self, request, queryset, view):
        queryset = queryset \
            .annotate(count=Count('tag_travel_records')
                      ) \
            .order_by('-count')
        return queryset


class TagApis(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    filter_backends = [TagFilterBackend, DjangoFilterBackend]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=['GET'], detail=False, url_path='popular')
    def popular(self, request, *args, **kwargs):
        owner = _permission.user_check(request)
        if owner < 0:
            raise NotFound()
        other_tags = Tag.objects.all().exclude(Q(name__contains='市') | Q(name__contains='城区')
                                               | Q(name__contains='自治州') | Q(name__contains='省')
                                               | Q(name__contains='县'))
        size = other_tags.count()
        instance = other_tags.annotate(count=Count('tag_travel_records')).order_by('-count')[:size / 10]
        sample = random.sample(xrange(floor(size / 10)), 10)
        result = [instance[i] for i in sample]
        serializer = TagSerializer(result, many=True)
        data = serializer.data
        return Response({"result": data})
