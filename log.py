import logging.handlers
import datetime

g_logger = logging.getLogger('mylogger')
g_logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler('logger/all.log', when='midnight', interval=1, backupCount=7,
                                                       atTime=datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler('logger/error.log')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

g_logger.addHandler(rf_handler)
g_logger.addHandler(f_handler)
