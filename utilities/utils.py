# utils.py
import logging
import os
from datetime import datetime
from threading import Lock
from .config import LOG_DIR


class HTMLReportLogger:
    """_summary_

    Returns:
        _type_: _description_
    """
    def __init__(self):
        self.test_logs = {}
        self.current_test = None
        self.lock = Lock()
        
    def start_test_capture(self, test_name):
        """_summary_

        Args:
            test_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.lock:
            self.current_test = test_name
            self.test_logs[test_name] = []
            
    def end_test_capture(self, test_name):
        """_summary_

        Args:
            test_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.lock:
            self.current_tests = None
            
    def get_logs_for_test(self, test_name):
        """_summary_

        Args:
            test_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.lock:
            return "\n".join(self.test_logs.get(test_name, []))
        
    def log(self, level, message):
        """_summary_

        Args:
            level (_type_): _description_
            message (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.lock:
            if self.current_test:
                self.test_logs[self.current_test].append(f"{level}: {message}")
                
class CustomLogger(logging.Logger):
    """_summary_

    Args:
        logging (_type_): _description_

    Returns:
        _type_: _description_
    """
    def __init__(self, name: str, level=logging.NOTSET) -> None:
        super().__init__(name, level)
        self.html_logger = HTMLReportLogger()
        
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        """_summary_

        Args:
            level (_type_): _description_
            msg (_type_): _description_
            args (_type_): _description_
            exc_info (_type_, optional): _description_. Defaults to None.
            extra (_type_, optional): _description_. Defaults to None.
            stack_info (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        super()._log(level, msg, args, exc_info, extra, stack_info)
        self.html_logger.log(logging.getLevelName(level), msg % args if args else msg)
        
# Set up logging
def setup_logging():
    """_summary_

    Returns:
        _type_: _description_
    """
    # Ensure the log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # Create a timestamp for the log file name
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(LOG_DIR, f'log_{timestamp}.log')

    # Setup logging
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to Logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized. Log File: {log_file}")

    return logger


# Create a global logger instance
logger = setup_logging()

def start_test_capture(test_name):
    logger.html_logger.start_test_capture(test_name)
    
def end_test_capture(test_name):
    logger.html_logger.end_test_capture(test_name)
    
def get_logs_for_test(test_name):
    return logger.html_logger.get_logs_for_test(test_name)