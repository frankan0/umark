class Article:

    title =''
    originFilePath =''
    ctime = 0
    destFilePath = ''

    def __init__(self,title,originFilePath,destFilePath,ctime):
        self.title = title
        self.originFilePath = originFilePath
        self.destFilePath = destFilePath
        self.ctime = ctime

        