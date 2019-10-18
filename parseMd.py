import os 
import sys
from ftputil import MyFTP
import parseHelper
from fileUtil import FileUtil

upload = True;
## 基础目录
baseDir = os.getcwd();
baseDir = "/Users/frank0/OneDrive/documents/note/";
ignoreDir = ["working"];
## 解析markdown
articles = [];
baseWriteDir = '/Users/frank0/articles/';
#处理图片目录
imageDir = "/Users/frank0/OneDrive/documents/note/images/";
destDir = "/Users/frank0/articles/images/";
## 生成index.html文件
websiteTitle = "弗兰克零的网络记事本";

fileUtil = FileUtil(ignoreDir);
fileUtil.traverse(baseDir);
articles = parseHelper.parse2Article(fileUtil.mdFiles,baseWriteDir);
parseHelper.generateIndexFile(articles,baseWriteDir,websiteTitle);
parseHelper.copyImages();

if upload:
    my_ftp = MyFTP("ip")
    my_ftp.login("username", "password")
    ## 上传至FTP服务器
    my_ftp.upload_file_tree(baseWriteDir,"./")
    my_ftp.close();






