from logger.custom_logging import CustomLogger

# Create a singleton logger instance
_logger_instance = CustomLogger()

def get_logger(name=__file__):
    """Get a structured logger instance"""
    return _logger_instance.get_logger(name)