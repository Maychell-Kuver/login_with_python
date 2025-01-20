from logging.handlers import RotatingFileHandler
import logging

log_rotate_handler = RotatingFileHandler("app.log", maxBytes=10485760, backupCount=10)
log_rotate_handler.setFormatter(logging.Formatter('%(asctime)s | %(name)-13s | %(levelname)-7s | [%(funcName)s:%(lineno)d] => %(message)s'))

log_command = logging.getLogger()
log_command.setLevel('DEBUG')
log_command.addHandler(log_rotate_handler)
