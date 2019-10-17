import markdown
import codecs
import os 
import sys
from jinja2 import Environment, FileSystemLoader,select_autoescape
from ftplib import FTP
import sys
from ftputil import MyFTP
import time
import shutil


jinja_environment = Environment(autoescape=False,
    loader=FileSystemLoader('./templates'))

## 生成index目录页
## 基础目录
baseDir = os.getcwd();
baseDir = "/Users/frank0/OneDrive/documents/note/";
## 遍历目录
## 生成数据格式为:  
#  key-> '/learning',value->['ssss.md','sdfsdf.md']
#  key-> '/learning/test',value->['ssss.md','sdfsdf.md']

directory = {};
filterDir = ["working"];

def ignoreDir(name):
    result = False
    for dir in filterDir:
        if name == dir:
            result = True
            break
    return result

def traverse(f):
    fs = os.listdir(f)
    for f1 in fs:
        if f1.startswith('.'):
            continue;
        if ignoreDir(f1):
            continue;
        tmp_path = os.path.join(f,f1)
        if not os.path.isdir(tmp_path):
            print('文件: %s'%tmp_path)
            try:
                fo = open(tmp_path, "r+")
                if not fo.name.endswith(".md"):
                    continue;
                files = directory.get(f);
                if files is None:
                    files = [];
                files.append(fo.name);
                directory[f] = files;
            finally:
                fo.close();
        else:
            print('文件夹：%s'%tmp_path)
            traverse(tmp_path);        

path = baseDir;
traverse(path)

print(directory);

## 解析markdown
articles = [];
baseWriteDir = '/Users/frank0/articles/';
for (key,value) in directory.items():
    for originFileName in value:
        ofn = originFileName.split('/');
        fileName = ofn[len(ofn) - 1];
        t = fileName.split('.');
        articleTitle = t[0];
        fileName = fileName.replace('md','html');
        sourceFileName = originFileName;
        input_file = codecs.open(sourceFileName, mode="r", encoding="utf-8")
        text = input_file.read();
        input_file.close();
        articleHtml = markdown.markdown(text,extensions=["fenced_code","tables"]);
        #最后修改日期
        statinfo=os.stat(sourceFileName);
        time_local = time.localtime(statinfo.st_mtime)
        mtime = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        #作者
        author = "弗兰克零";
        ## 写入文件html文件 可以使用模板引擎进行渲染
        template = jinja_environment.get_template('article_template.html');
        htmlTemplate = template.render({'articleTitle': articleTitle,'articleContent':articleHtml,'mtime':mtime,'author':author});
    
        # 处理相对路径的图片，绝对路径以HTTP开头的不处理
        htmlTemplate = htmlTemplate.replace("src=\"../../","src=\"./");
        ## 写入文件
        rf = baseWriteDir + fileName;
        articles.append(fileName);
        output_file = codecs.open(rf, "w",
                                encoding="utf-8",
                                errors="xmlcharrefreplace"
        );
        output_file.write(htmlTemplate);

#处理图片目录
imageDir = "/Users/frank0/OneDrive/documents/note/images/";
destDir = "/Users/frank0/articles/images/";
alllist=os.listdir(imageDir)
for f1 in alllist:
    if f1.startswith('.'):
            continue;
    tmp_path = os.path.join(imageDir,f1)
    if not os.path.isdir(tmp_path):
        print('图片: %s'%tmp_path)       
        shutil.copyfile(tmp_path, destDir+f1)

## 生成index.html文件
websiteTitle = "弗兰克零的网络记事本";
template = jinja_environment.get_template('catalog_template.html');
htmlTemplate = template.render({'articles': articles,'websiteTitle':websiteTitle});
## 写入文件
fileName = "index.html";
rf = baseWriteDir + fileName;
articles.append(fileName);
output_file = codecs.open(rf, "w",
                        encoding="utf-8",
                        errors="xmlcharrefreplace"
);
output_file.write(htmlTemplate);
my_ftp = MyFTP("172.96.237.147")
my_ftp.login("blog_onenavigation", "pjEHTDMKRbXPeAxj")
## 上传至FTP服务器
my_ftp.upload_file_tree(baseWriteDir,"./")
my_ftp.close();






