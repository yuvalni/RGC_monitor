import logging
import os
from logging.handlers import TimedRotatingFileHandler
from shutil import copyfile
from datetime import datetime


class MyLogger(object):

    def __init__(self, name, file, level, when, interval, backup_count, formatter, header, save_path):
        self.name = name
        self.formatter = formatter
        self.file = file
        self.when = when
        self.interval = interval
        self.backupCount = backup_count
        self.level = level
        self.header = header
        self.savePath = save_path

        if self.header != "":
            self.logHandler = MyTimedRotatingFileHandler(self.file, self.when, self.interval, self.backupCount)
        else:
            self.logHandler = TimedRotatingFileHandler(self.file, self.when, self.interval, self.backupCount)

        self.logHandler.setFormatter(self.formatter)

        self.logger = logging.getLogger(self.name)
        self.logger.propagate = False  # this will make the logs done to this logger not show up in the root logger.
        self.logger.setLevel(self.level)

        if self.header != "":
            self.logHandler.configureHeaderWriter(self.header, self.logger, self.savePath)

        self.logger.addHandler(self.logHandler)

        if self.header != "":
            if not os.path.exists(self.file):
                self.logger.info(self.header)


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, logfile, when, interval, backupCount):
        super(MyTimedRotatingFileHandler, self).__init__(logfile, when, interval, backupCount)
        self._header = ""
        self._log = None
        self.savePath = ""

    def doRollover(self):
        src = self.MygetFilesToCopy()
        for s in src:
            dirName, baseName = os.path.split(self.baseFilename)
            prefix = self.baseFilename + "."
            suffix = s[len(prefix):]
            dst = self.savePath + "\\" + baseName + "." + suffix
            try:
                copyfile(s, dst)
                print("File copied successfully:" + s)

            except:
                print("Error occurred while copying file.")

        super(MyTimedRotatingFileHandler, self).doRollover()
        if self._log is not None and self._header != "":
            self._log.info(self._header)

    def setHeader(self, header):
        self._header = header

    def configureHeaderWriter(self, header, log, save_path):
        self._header = header
        save_path = os.fspath(save_path)
        # keep the absolute path, otherwise derived classes which use this
        # may come a cropper when the current directory changes
        self.savePath = os.path.abspath(save_path)
        self._log = log

    def MygetFilesToCopy(self):
        """
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount + 1]
        return result