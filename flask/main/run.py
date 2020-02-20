# coding=utf-8
#############################################
#  DEPENDANCE
#############################################
from flask import Flask
from flask import render_template
from flask import request        
app = Flask(__name__)


import paramiko
ssh = paramiko.SSHClient()

import re
import os
import pexpect
import time
import numpy as np

from sub_modu import *
from vars_common import *

#############################################
# >>> root
@app.route('/' , methods=["GET","POST"])
#############################################
def index():
 cap_item, todo_item ,memo_item  = category_from_dir(EVERYDAY_DIR)
 blog_item = get_dir_filelist_and_each_content(BLOG_DIR)
 all_item = np.concatenate((cap_item , blog_item) ,axis=0)
 item_num = len(all_item)
 ####################
 #整理文件的函数
 #split_capture_org()
 #split_everyday_org()
 return render_template('index.html',
                        posts_key =get_dir_filelist(ARTICLE),
                        item_num = item_num,
                        todo_item=todo_item,
                        cap_item = all_item)
#############################################
# >>> memo 
@app.route('/memo/', methods=["GET","POST"])
#############################################
def memo():
 if request.method == 'POST' and request.form.get("memo_chk_sta"):
  return back_from_browser(RECORD_BACK)
 else :
  cap_item, todo_item, memo_item = category_from_dir(EVERYDAY_DIR)
  return render_template('memo.html',memo_item=memo_item)


#############################################
# >>> capture
@app.route('/capture/', methods=["GET","POST"])
#############################################
def capture():
 if request.method == 'POST' and request.form.get("passtext"):
  everyday_file = EVERYDAY_DIR + time.strftime("%Y-%m-%d-%H-%M-%S") + ".org"
  return render_template('capture.html', textcontent=get_dir_filelist_and_each_content(EVERYDAY_DIR), latest_commit_content=proc_req_record(everyday_file))
 else:
   return render_template('capture.html',textcontent=get_dir_filelist_and_each_content(EVERYDAY_DIR), latest_commit_content= "no commit")

#############################################
# >>> article
@app.route('/article/<html_name>', methods=["GET","POST"])
#############################################
def article(html_name):
 if(html_name != 'index'):
  filepath = ARTICLE + html_name
  return render_template('article_show.html', textcontent=get_file_content(filepath),title=get_dir_filelist(ARTICLE))
 elif request.method == 'POST' :
  everyday_file = ARTICLE + time.strftime("%y-%m-%d-%H-%M-%S") + request.form.get("text_head")+".org"
  w_text = request.form.get("text_body").encode('utf-8')
  print everyday_file
  # 对于中文文件名，windows默认都是gbk，为了兼容windows下中文标题，统一用gbk编码文件标题。
  filename = everyday_file.encode('gbk')
  with open(filename , 'w') as f:
   f.write(w_text)
   f.write("\n")
   f.close()
  return render_template('article.html', textcontent=get_dir_filelist(ARTICLE))
 else:
  return render_template('article.html',textcontent=get_dir_filelist(ARTICLE))
#############################################
# >>> z_blog
@app.route('/z_blog/<html_name>')
#############################################
def blog(html_name):
 return app.send_static_file("html/z_blog/%s"%html_name.encode('utf-8'))


#############################################
# >>> z_todo
@app.route('/z_todo/<html_name>')
#############################################
def todo(html_name):
 return app.send_static_file("html/z_todo/%s"%html_name.encode('utf-8'))


#############################################
# >>> z_frontPage
@app.route('/z_frontPage/<html_name>')
#############################################
def frontPage(html_name):
 return app.send_static_file("html/z_frontPage/%s"%html_name.encode('utf-8'))

#############################################
# >>> z_org
@app.route('/z_org/<html_name>')
#############################################
def org(html_name):
 return app.send_static_file("html/z_org/%s"%html_name.encode('utf-8'))

#############################################
# >>> req_data
@app.route('/req_data/<dest>',methods=["GET"])
#############################################
def info(dest):
 if request.method=='GET':
  if(dest=="ws") :
   #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #ssh.connect(hostname='10.0.0.2', port=22, username='fixer', password='g')
   #cmd = 'builtin cd lzh ;git st'
   #stdin,stdout,stderr = ssh.exec_command(cmd)
   #msg = stdout.read()
   #msg = msg.decode('utf-8')
   #return msg
   return "msg"
  elif(dest=="sv") :
   #output =os.popen('cd '+USERDIR+'; git status')
   output=os.popen(CAP_PL)
   msg1 = output.read()
   return "msg1"




if __name__ == '__main__':
 app.run(debug=True)

