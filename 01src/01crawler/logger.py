import logging
import datetime
import os

class Logger(object):
    '''
    record the log when u want
    u need to create a folder log under the folder tool
    problem may be found using spyder, use cmd instead
    '''
    def __init__(self, loggerFolder ="log\\", exeFileName="", level=logging.DEBUG):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        if not os.path.exists(loggerFolder):
            os.makedirs(loggerFolder, exist_ok=True)
        fmt = '%(asctime)-15s %(filename)s[line:%(lineno)d] - %(levelname)s - %(name)s : %(message)s'
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter(fmt=fmt)
            streamHandler  = logging.StreamHandler()
            streamHandler.setFormatter(formatter)
            streamHandler.setLevel(logging.INFO)
            self.logger.addHandler(streamHandler)
            
            logRecordFile = os.path.join(loggerFolder, exeFileName+"_"+datetime.datetime.now().strftime("%Y-%m-%d.log"))
            fileHandler=logging.FileHandler(logRecordFile, encoding='utf-8')
            fileHandler.setFormatter(formatter)
            fileHandler.setLevel(logging.DEBUG)
            self.logger.addHandler(fileHandler)

        
        
    def debug(self,msg):
        self.logger.debug(msg)
    
    def info(self, msg):
        self.logger.info(msg)

    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
        
    def critical(self, msg):
        self.logger.critical(msg)
        
    def log(self, level, msg):
        self.logger.log(level, msg)
        
    def setLevel(self, level):
        self.logger.setLevel(level)
        
    def disable(self):
        logging.disable(50) 
        