#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Article:

    title =''
    originFilePath =''
    ctime = 0
    destFilePath = ''
    fileName = ''

    def __init__(self,title,fileName,originFilePath,destFilePath,ctime):
        self.title = title
        self.fileName = fileName
        self.originFilePath = originFilePath
        self.destFilePath = destFilePath
        self.ctime = ctime


        