from django.conf import settings
from functools import lru_cache


class ConfigWrapper:
    def __init__(self):
        try:
            from constance import config as constance_config
            from constance import settings as constance_settings

            self.constance_config = constance_config
            self.constance_settings = constance_settings
        except ImportError:
            self.constance_config = None
            self.constance_settings = None

    @lru_cache(maxsize=None)
    def __getattr__(self, key):
        if self.constance_config:
            try:
                result = getattr(self.constance_config, key)
                if result is not None:
                    return result
            except AttributeError:
                pass
        return getattr(settings, key)

    def reset(self):
        self.__getattr__.cache_clear()
        if self.constance_settings:
            for name, options in self.constance_settings.CONFIG.items():
                setattr(self.constance_config, name, options[0])


config = ConfigWrapper()
