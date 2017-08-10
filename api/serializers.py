from rest_framework import serializers
from .v0.model01 import TransportTemp, STATUS_CHOICES


class TempSerializer(serializers.Serializer):

    # t_ - transport attribute
    t_c_status = serializers.IntegerField(choices=STATUS_CHOICES)

    # e_ - employee attribute
    t_e_uuid = serializers.UUIDField(default=None)
    t_e_name = serializers.CharField(max_length=128, default=None)
    t_e_surname = serializers.CharField(max_length=128, default=None)
    t_e_patronymic = serializers.CharField(max_length=128, default=None)
    t_e_begin_contract = serializers.DateField(default=None)
    t_e_end_contract = serializers.DateField(default=None)

    # c_ - corporate attribute
    t_c_uuid = serializers.UUIDField(default=None)
    t_c_company_name = serializers.CharField(max_length=128, default=None)
    t_c_name_corp_level_0 = serializers.CharField(max_length=128, default=None)
    t_c_name_corp_level_1 = serializers.CharField(max_length=128, default=None)
    t_c_name_corp_level_2 = serializers.CharField(max_length=128, default=None)
    t_c_name_corp_level_3 = serializers.CharField(max_length=128, default=None)
    t_c_position_name = serializers.CharField(max_length=128, default=None)

    def create(self, validated_data):

        return TransportTemp.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.t_c_status = validated_data.get('t_c_status', instance.t_c_status)

        instance.t_e_uuid = validated_data.get('t_e_uuid', instance.t_e_uuid)
        instance.t_e_name = validated_data.get('t_e_name', instance.t_e_name)
        instance.t_e_surname = validated_data.get('t_e_surname', instance.t_e_surname)
        instance.t_e_patronymic = validated_data.get('t_e_patronymic', instance.t_e_patronymic)
        instance.t_e_begin_contract = validated_data.get('t_e_begin_contract', instance.t_e_begin_contract)
        instance.t_e_end_contract = validated_data.get('t_e_end_contract', instance.t_e_end_contract)

        instance.t_c_uuid = validated_data.get('t_c_uuid', instance.t_c_uuid)
        instance.t_c_company_name = validated_data.get('t_c_company_name', instance.t_c_company_name)
        instance.t_c_name_corp_level_0 = validated_data.get('t_c_name_corp_level_0', instance.t_c_name_corp_level_0)
        instance.t_c_name_corp_level_1 = validated_data.get('t_c_name_corp_level_1', instance.t_c_name_corp_level_1)
        instance.t_c_name_corp_level_2 = validated_data.get('t_c_name_corp_level_2', instance.t_c_name_corp_level_2)
        instance.t_c_name_corp_level_3 = validated_data.get('t_c_name_corp_level_3', instance.t_c_name_corp_level_3)
        instance.t_c_position_name = validated_data.get('t_c_position_name', instance.t_c_position_name)
        instance.save()

        return instance
