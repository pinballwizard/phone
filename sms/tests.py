from django.test import TestCase
from sms.views import process_sms_text
import pymssql


class SMSTextParseTest(TestCase):
    def test_regex_top_boundary(self):
        self.assertCountEqual(
            process_sms_text('0000000000000000000').group(0),
            '0000000000000000000',
            "Регулярное выражение не распознает 19 цифр"
        )

    def test_regex(self):
        self.assertCountEqual(
            process_sms_text('Показания впу л/с 111020514560 абыр абыр').group(0),
            '111020514560',
            "Регулярное выражение не распознает тестовую смс"
        )

    def test_regex_bottom_boundary(self):
        self.assertCountEqual(
            process_sms_text('0000000000').group(0),
            '0000000000',
            "Регулярное выражение не распознает 10 цифр"
        )

    def test_regex_less_then(self):
        self.assertIsNone(
            process_sms_text('000000000'),
            "Регулярное выражение распознает меньше 10 цифр"
        )

    def test_regex_more_then(self):
        self.assertIsNone(
            process_sms_text('00000000000000000000'),
            "Регулярное выражение распознает больше 19 цифр"
        )


class SmsMssqlConnectionTest(TestCase):
    def test_database_connection(self):
        conn_data = {
            'server': 'ksql02.ksk.loc:1434',
            'user': 'rd',
            'password': 'L151?t%fr',
            'database': 'DataForSMS',
        }
        result = False
        try:
            with pymssql.connect(**conn_data) as connection:
                with connection.cursor() as cursor:
                    if cursor:
                        result = True
        except:
            result = False
        finally:
            self.assertTrue(result, "Подключение к базе не удалось")