import os
import logging.config


class LoggerSetup:
    _is_configured = False

    @classmethod
    def setup_logging(cls, config_dir='app/config', config_file='logging.ini'):
        if not cls._is_configured:
            config_path = os.path.join(config_dir, config_file)
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Logging config not found: {config_path}")
            logging.config.fileConfig(config_path)
            cls._is_configured = True

    @classmethod
    def get_logger(cls, name):
        cls.setup_logging()
        return logging.getLogger(name)
