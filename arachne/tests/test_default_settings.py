from unittest import TestCase


class TestDefaultSettings(TestCase):

    def test_settings(self):
        from arachne import default_settings

        self.assertIsNone(default_settings.TELNETCONSOLE_PORT)
        self.assertEquals(default_settings.USER_AGENT,
                          'Arachne (+http://github.com/kirankoduru/arachne)')
        self.assertEquals(default_settings.EXPORT_PATH, 'exports/')
        self.assertFalse(default_settings.EXPORT_JSON)
        self.assertFalse(default_settings.EXPORT_CSV)
        self.assertFalse(default_settings.LOGS)
        self.assertEquals(default_settings.LOGS_PATH, 'logs/')
        self.assertTrue(default_settings.DEBUG)
        self.assertTrue(isinstance(default_settings.SCRAPY_SETTINGS, dict))
