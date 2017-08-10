from django.db import models
# Create your models here.

STATUS_CHOICES = (
    # 1 - 5 employee status
    (0, 'Change credential'),           # Изменение учетных данных
    (1, 'To lay off'),                  # Увольнение
    (2, 'Recruit'),                     # Прием
    (3, 'Transfer'),                    # Изменение должности
    (4, 'Maternity leave'),             # Декретный отпуск
    (5, 'Holiday'),                     # Отпуск
    # 6 - 12 corporate structure status
    (6, 'Change credential'),           # Переименование подразделения
    (7, 'Abolish a unit'),              # Упразднение подразделения
    (8, 'Create a unit'),               # Создание подразделения
    (9, 'Transfer a unit'),             # Изменение подчиненности
    (10, 'Add the position'),           # Добавление позиции
    (11, 'Reduce the position'),        # Сокращение позиции
    (12, 'Transfer a unit'),            # Изменение подчиненности
)


class TransportTemp(models.Model):

    # t_ - temp
    # s_ - service attribute
    t_s_author = models.ForeignKey('auth.User')
    t_s_number_transaction = models.AutoField(primary_key=True)
    t_s_time_transaction = models.DateTimeField(auto_now_add=True)

    # t_ - transport attribute
    t_c_status = models.IntegerField(choices=STATUS_CHOICES)

    # e_ - employee attribute
    t_e_uuid = models.UUIDField(default=None)
    t_e_name = models.CharField(max_length=128, default=None)
    t_e_surname = models.CharField(max_length=128, default=None)
    t_e_patronymic = models.CharField(max_length=128, default=None)
    t_e_begin_contract = models.DateField(default=None)
    t_e_end_contract = models.DateField(default=None)

    # c_ - corporate attribute
    t_c_uuid = models.UUIDField(default=None)
    t_c_company_name = models.CharField(max_length=128, default=None)
    t_c_name_corp_level_0 = models.CharField(max_length=128, default=None)
    t_c_name_corp_level_1 = models.CharField(max_length=128, default=None)
    t_c_name_corp_level_2 = models.CharField(max_length=128, default=None)
    t_c_name_corp_level_3 = models.CharField(max_length=128, default=None)
    t_c_position_name = models.CharField(max_length=128, default=None)

    def __str__(self):
        return sorted(
            {'service_attribute':
                 [self.t_s_author, self.t_s_number_transaction, self.t_s_time_transaction],
             'transport_attribute':
                 [self.t_c_status],
             'employee_attribute':
                 [self.t_e_uuid, self.t_e_name, self.t_e_surname, self.t_e_patronymic,
                  self.t_e_begin_contract, self.t_e_end_contract],
             'corporate_attribute':
                 [self.t_c_uuid, self.t_c_company_name, self.t_c_name_corp_level_0, self.t_c_name_corp_level_1,
                  self.t_c_name_corp_level_2, self.t_c_name_corp_level_3, self.t_c_position_name]
            }
        )

    def as_json(self):
        return dict(
            t_s_author=self.t_s_author,
            t_s_number_transaction=self.t_s_number_transaction,
            t_s_time_transaction=self.t_s_time_transaction,
            t_c_status=self.t_c_status,

            t_e_uuid=self.t_e_uuid,
            t_e_name=self.t_e_name,
            t_e_surname=self.t_e_surname,
            t_e_patronymic=self.t_e_patronymic,
            t_e_begin_contract=self.t_e_begin_contract,
            t_e_end_contract=self.t_e_end_contract,

            t_c_uuid=self.t_c_uuid,
            t_c_company_name=self.t_c_company_name,
            t_c_name_corp_level_0=self.t_c_name_corp_level_0,
            t_c_name_corp_level_1=self.t_c_name_corp_level_1,
            t_c_name_corp_level_2=self.t_c_name_corp_level_2,
            t_c_name_corp_level_3=self.t_c_name_corp_level_3,
            t_c_position_name=self.t_c_position_name
        )


class TransportPerson(models.Model):

    # p_ - person
    p_id = models.AutoField(primary_key=True)
    p_uuid = models.UUIDField(default=None)
    p_name = models.CharField(max_length=128, default=None)
    p_surname = models.CharField(max_length=128, default=None)
    p_patronymic = models.CharField(max_length=128, default=None)

    def __str__(self):
        return ' '.join([
            self.p_id,
            self.p_uuid,
            self.p_name,
            self.p_surname,
            self.p_patronymic,
        ])

    def as_json(self):
        return dict(
            p_id=self.p_id,
            p_uuid=self.p_uuid,
            p_name=self.p_name,
            p_surname=self.p_surname,
            p_patronymic=self.p_patronymic,
        )


class TransportEmployee(models.Model):

    # e_ employee
    e_id = models.AutoField(primary_key=True)
    e_begin_contract = models.DateField(default=None)
    e_end_contract = models.DateField(default=None)
    e_status = models.IntegerField(choices=STATUS_CHOICES[0:6])

    def __str__(self):
        return ' '.join([
            self.e_id,
            self.e_status,
            self.e_begin_contract.__str__(),
            self.e_end_contract.__str__(),
        ])

    def as_json(self):
        return dict(
            e_id=self.e_id,
            e_begin_contract=self.e_begin_contract,
            e_end_contract=self.e_end_contract,
            e_status=self.e_status
        )


class TransportStructure(models.Model):

    # s_ - structure
    s_id = models.AutoField(primary_key=True)
    s_uuid = models.UUIDField(default=None)
    s_company_name = models.CharField(max_length=128, default=None)
    s_name_corp_level_0 = models.CharField(max_length=128, default=None)
    s_name_corp_level_1 = models.CharField(max_length=128, default=None)
    s_name_corp_level_2 = models.CharField(max_length=128, default=None)
    s_name_corp_level_3 = models.CharField(max_length=128, default=None)
    s_position_name = models.CharField(max_length=128, default=None)
    s_status = models.IntegerField(choices=STATUS_CHOICES[6:12])

    def __str__(self):
        return ' '.join([
            self.s_id,
            self.s_uuid,
            self.s_company_name,
            self.s_name_corp_level_0,
            self.s_name_corp_level_1,
            self.s_name_corp_level_2,
            self.s_name_corp_level_3,
            self.s_position_name,
            self.s_status
        ])

    def as_json(self):
        return dict(
            s_id=self.s_id,
            s_uuid=self.s_uuid,
            s_company_name=self.s_company_name,
            s_name_corp_level_0=self.s_name_corp_level_0,
            s_name_corp_level_1=self.s_name_corp_level_1,
            s_name_corp_level_2=self.s_name_corp_level_2,
            s_name_corp_level_3=self.s_name_corp_level_3,
            s_position_name=self.s_position_name,
            s_status=self.s_status
        )
