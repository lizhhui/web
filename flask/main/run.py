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
 ####################
 # todo is committing
 if request.method == 'POST' and request.form.get("finish"):
  category_to_dir(EVERYDAY_DIR+request.form.get("finish")+".org",DELETE_DIR)
 elif request.method == 'POST' and request.form.get("remove"):
  category_to_dir(DELETE_DIR+request.form.get("remove")+".org",TRASH_DIR)
 elif request.method == 'POST' and request.form.get("pullback"):
  category_to_dir(DELETE_DIR+request.form.get("pullback")+".org",EVERYDAY_DIR)
 ####################
 # 
 cap_item, todo_item ,memo_item = category_from_dir(EVERYDAY_DIR)
 del_cap,del_todo,del_memo = category_from_dir(DELETE_DIR)
 blog_item = get_dir_filelist_and_each_content(BLOG_DIR)
 all_item = np.concatenate((cap_item , blog_item) ,axis=0)
 item_num = len(all_item)
 #delete_item = np.concatenate((del_cap,del_memo) ,axis=0)
 delete_item = del_cap

 _,tag_dict=extract_tag_from_dir(ARTICLE)
 ####################
 #整理文件的函数
 #split_capture_org()
 #split_everyday_org()
 return render_template('index.html',
                        article_files   = get_dir_filelist(ARTICLE),
                        article_tags    = tag_dict,
                        item_num    = item_num,
                        todo_item   = todo_item,
                        finish_item = del_todo,
                        delete_item = delete_item,
                        cap_item    = all_item)
#############################################
# >>> memo 
@app.route('/memo/', methods=["GET","POST"])
#############################################
def memo():
 # category memo is committing
 if request.method == 'POST' and request.form.get("finish"):
  category_to_dir(EVERYDAY_DIR+request.form.get("finish")+".org",DELETE_DIR)
 elif request.method == 'POST' and request.form.get("remove"):
  category_to_dir(DELETE_DIR+request.form.get("remove")+".org",TRASH_DIR)
 elif request.method == 'POST' and request.form.get("pullback"):
  category_to_dir(DELETE_DIR+request.form.get("pullback")+".org",EVERYDAY_DIR)
 elif request.method == 'POST' and request.form.get("memo_chk_sta"):
  update_memo_file(RECORD_BACK)
 #template
 _,_, memo_item = category_from_dir(EVERYDAY_DIR)
 _,_,del_memo = category_from_dir(DELETE_DIR)
 i=0
 temp =[]
 for kk in memo_item:
  temp.append(["","",[],""])
  temp[-1][0]=kk[0]
  temp[-1][1]=kk[1]
  temp[-1][2]=kk[2]
  temp[-1][3]=i
  i=i+1
 return render_template('memo.html',memo_item=temp,delete_item=del_memo)


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
 if request.method == 'POST' and request.form.get("text_head") :
  everyday_file = ARTICLE + time.strftime("%Y-%m-%d-%H-%M-%S") + request.form.get("text_head")+".org"
  w_text = request.form.get("text_body").encode('utf-8')
  print everyday_file
  # 对于中文文件名，windows默认都是gbk，为了兼容windows下中文标题，统一用gbk编码文件标题。
  filename = everyday_file.encode('utf-8')
  with open(filename , 'w') as f:
   f.write(w_text)
   f.write("\n")
   f.close()
  file_dict,tag_dict=extract_tag_from_dir(ARTICLE)
  return render_template('article.html',tag_dict = tag_dict,file_dict=file_dict)

 elif request.method == 'POST' and request.form.get("text_body") :
  with open(ARTICLE + html_name,'w') as f:
   f.write(request.form.get("text_body").encode('utf-8'))
   f.write("\n")
   f.close()
  file_dict,tag_dict=extract_tag_from_dir(ARTICLE)
  return render_template('article.html',tag_dict = tag_dict,file_dict=file_dict)

 elif request.method == 'POST' and request.form.get("remove") :
  category_to_dir(ARTICLE+request.form.get("remove"),TRASH_DIR)
  file_dict,tag_dict=extract_tag_from_dir(ARTICLE)
  return render_template('article.html',tag_dict = tag_dict,file_dict=file_dict)

 elif(html_name == 'index'):
  file_dict,tag_dict=extract_tag_from_dir(ARTICLE)
  return render_template('article.html',tag_dict = tag_dict,file_dict=file_dict)

 elif(re.match(r'^\d{4}-\d{2}-\d{2}.*',html_name)): 
  filepath = ARTICLE + html_name
  file_dict,tag_dict=extract_tag_from_dir(ARTICLE)
  return render_template('article_show.html',
                         title=html_name,
                         textcontent=get_file_content(filepath),
                         tags = file_dict[html_name],
                         tag_dict = tag_dict,
                         file_dict=file_dict)
 else:
  file_dict,tag_dict=extract_tag_from_dir(ARTICLE)
  return render_template('article_tag.html',
                         title="TAG:"+html_name,
                         filelists=tag_dict[html_name],
                         tag_dict = tag_dict,
                         file_dict=file_dict)

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

