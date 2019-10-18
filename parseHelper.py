
from article import Article
import time
import shutil
from jinja2 import Environment, FileSystemLoader,select_autoescape
import markdown
import codecs
import os
import platform
import collections
## 模板配置
jinja_environment = Environment(autoescape=False,loader=FileSystemLoader('./templates'))

## 基础配置
imageDir = "/Users/frank0/OneDrive/documents/note/images/";
destDir = "/Users/frank0/articles/images/";

def parse2Article(mdFiles={},baseWriteDir=""):
    articles = [];
    for (key,value) in mdFiles.items():
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
            # 获取创建日期
            time_local = time.localtime(get_creation_date(sourceFileName))
            ctime = time_local
            #作者
            author = "弗兰克零";
            ## 写入文件html文件 可以使用模板引擎进行渲染
            template = jinja_environment.get_template('article_template.html');
            htmlTemplate = template.render({'articleTitle': articleTitle,'articleContent':articleHtml,'mtime':time.strftime("%Y-%m-%d",ctime),'author':author});
            # 处理相对路径的图片，绝对路径以HTTP开头的不处理
            htmlTemplate = htmlTemplate.replace("src=\"../../","src=\"./");
            ## 写入文件
            rf = baseWriteDir + fileName;
            output_file = codecs.open(rf, "w",
                                    encoding="utf-8",
                                    errors="xmlcharrefreplace"
            );
            output_file.write(htmlTemplate);
            article = Article(articleTitle,fileName,sourceFileName,rf,ctime);
            articles.append(article);
    return articles        

def generateIndexFile(articles = [],baseWriteDir="",websiteTitle = '网络记事本'):

    ## 按照时间分类并排序，越早的越靠前
    sortArticle = {};
    for  a in articles:
        sk = time.strftime("%Y%m",a.ctime)
        ass = sortArticle.get(sk);
        if ass is None:
            ass = [];
        ass.append(a);
        sortArticle[sk] = ass; 
    ## 排序
    sortArticle = collections.OrderedDict(sorted(sortArticle.items(),key=lambda obj:obj[0],reverse=True))
    ## 生成index.html文件
    template = jinja_environment.get_template('catalog_template.html');
    htmlTemplate = template.render({'articles': sortArticle,'websiteTitle':websiteTitle});
    ## 写入文件
    fileName = "index.html";
    indexFileLocation = baseWriteDir + fileName;
    articles.append(fileName);
    output_file = codecs.open(indexFileLocation, "w",
                            encoding="utf-8",
                            errors="xmlcharrefreplace"
    );
    output_file.write(htmlTemplate);

def copyImages():
    alllist=os.listdir(imageDir)
    for f1 in alllist:
        if f1.startswith('.'):
                continue;
        tmp_path = os.path.join(imageDir,f1)
        if not os.path.isdir(tmp_path):     
            shutil.copyfile(tmp_path, destDir+f1)


def get_creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime





    