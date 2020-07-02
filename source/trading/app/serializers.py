import uuid
from datetime import datetime as dt

import pytz
from rest_framework import serializers, fields

from app.models import Company, DailyPrice


class CompanySerializer(serializers.Serializer):

    company_id = fields.UUIDField(read_only=True)
    sector = fields.ChoiceField(choices=Company.SECTOR_TYPES, required=True)
    address = fields.CharField(max_length=200, required=True)
    symbol = fields.CharField(max_length=10, required=True)
    short_name = fields.CharField(max_length=20, required=True)

    def create(self, validated_data):
        validated_data['company_id'] = uuid.uuid4()
        return Company.objects.create(**validated_data)


class DailyPriceSerializer(serializers.Serializer):

    symbol = fields.CharField(max_length=10, required=True)

    open = fields.DecimalField(max_digits=15, decimal_places=4, required=True)
    high = fields.DecimalField(max_digits=15, decimal_places=4, required=True)
    low = fields.DecimalField(max_digits=15, decimal_places=4, required=True)
    close = fields.DecimalField(max_digits=15, decimal_places=4, required=True)

    volume = fields.IntegerField(min_value=0, required=True)

    date = fields.DateField(read_only=True)

    def create(self, validated_data):
        validated_data['date'] = dt.now(tz=pytz.UTC)

        return DailyPrice.objects.create(**validated_data)