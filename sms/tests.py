from django.test import TestCase
from sms.views import process_sms_text


class SMSTextParseTest(TestCase):

    def test_regex(self):
        self.assertCountEqual(
            process_sms_text('0000000000000000000').group(0),
            '0000000000000000000',
            "Регулярное выражение не распознает 19 цифр"
        )
        self.assertCountEqual(
            process_sms_text('Показания впу л/с 111020514560 абыр абыр').group(0),
            '111020514560',
            "Регулярное выражение не распознает тестовую смс"
        )
        self.assertCountEqual(
            process_sms_text('0000000000').group(0),
            '0000000000',
            "Регулярное выражение не распознает 10 цифр"
        )
        self.assertIsNone(
            process_sms_text('000000000'),
            "Регулярное выражение распознает меньше 10 цифр"
        )
        self.assertIsNone(
            process_sms_text('00000000000000000000'),
            "Регулярное выражение распознает больше 19 цифр"
        )

