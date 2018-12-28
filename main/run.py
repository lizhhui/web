
#!/usr/bin/python
# _*_ coding:utf-8 _*_
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

from sub_modu import *
from vars_common import *


@app.route('/' , methods=["GET","POST"])
def index():
 req_cmd = proc_req();
 everyday_file = Z_BLOG+time.strftime("%y-%m-%d")+".org"
 memo_item = proc_to_rem_file(REM_FILE)
 todo_item = proc_to_rem_file(TODO_FILE)
 cap_item  = proc_to_rem_file(CAP_FILE)
 if(req_cmd == 1) :
  return proc_req_pass();
 elif(req_cmd == 2) :
  return render_template('index.html', textcontent=proc_req_record(everyday_file) )
 elif(req_cmd == 3) :
  back_from_browser(RECORD_BACK);
  return "server received memo~"
 else:
  name = 'xxxx'
  return render_template('index.html', 
                         posts_key =gen_blog(BLOG_INDEX),
                         textcontent="",
                         memo_item=memo_item,
                         todo_item=todo_item,
                         cap_item = cap_item,
                         re_passwd=name)

@app.route('/z_blog/<html_name>')
def blog(html_name):
 #return "z_blog/{}".format(html_name)
 return app.send_static_file("z_blog/%s"%html_name.encode('utf-8'))
#return send_from_directory('/static',web.html)

@app.route('/z_todo/<html_name>')
def todo(html_name):
 return app.send_static_file("z_todo/%s"%html_name.encode('utf-8'))


@app.route('/z_frontPage/<html_name>')
def frontPage(html_name):
 return app.send_static_file("z_frontPage/%s"%html_name.encode('utf-8'))

@app.route('/z_org/<html_name>')
def org(html_name):
 return app.send_static_file("z_org/%s"%html_name.encode('utf-8'))

@app.route('/req_data/<dest>',methods=["GET"])
def info(dest):
 if request.method=='GET':
  if(dest=="ws") :
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect(hostname='10.0.0.2', port=22, username='fixer', password='g')
   cmd = 'builtin cd lzh ;git st'
   stdin,stdout,stderr = ssh.exec_command(cmd)
   msg = stdout.read()
   msg = msg.decode('utf-8')
   return msg
  elif(dest=="sv") :
   output =os.popen('cd '+USERDIR+'; git status')
   msg1 = output.read()
   return msg1




if __name__ == '__main__':
 app.run(debug=True)

