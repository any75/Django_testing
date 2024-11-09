import pytest
pytest_plugins = ['pytester']
def pytest_configure(config):
    config.option.django_settings_model = 'django_testing.settings'