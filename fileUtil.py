#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os 

class FileUtil:

    ignoreDirList = [];

    mdFiles = {}

    def __init__(self,ignoreDirList=[]):
        self.ignoreDirList = ignoreDirList;
        self.mdFiles = {}

    #忽律过滤文件
    def ignoreDir(self,name):
        result = False
        # 过滤隐藏文件
        if name.startswith('.'):
            return True
        for dir in self.ignoreDirList:
            if name == dir:
                result = True
                break
        return result

    #遍历目标目录，获取MD文件集合
    def traverse(self,dir):
        fs = os.listdir(dir)
        for f1 in fs:
            #过滤忽略目录    
            if self.ignoreDir(f1):
                continue;
            tmp_path = os.path.join(dir,f1)
            if not os.path.isdir(tmp_path):
                print('找到文件: %s'%tmp_path)
                try:
                    fo = open(tmp_path, "r+")
                    if not fo.name.endswith(".md"):
                        print("忽略文件 非md文件:%s"%tmp_path);
                        continue;
                    files = self.mdFiles.get(dir);
                    if files is None:
                        files = [];
                    files.append(fo.name);
                    self.mdFiles[dir] = files;
                finally:
                    fo.close();
            else:
                self.traverse(tmp_path); 