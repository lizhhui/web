#!/usr/bin/python
# _*_ coding:utf-8 _*_

import re
from flask import request
import os
import time
import shutil
from vars_common import *


################
# 已经不用了
################
def gen_blog(blog_index_path):
 posts_key=[]
 if(os.path.exists(blog_index_path)):
  with open(blog_index_path) as fp:
   str = fp.read()
   str = re.sub("\n"," ",str)
   str = re.sub(".*<ul",'<ul',str,1)
   str = re.sub("</ul>.*",'</ul>',str,1)
   str = re.sub("</a>","*",str)
   str = re.sub("<.*?>","",str).decode('utf-8')
   lll = str.split('*')
   for kk in lll :
    kk_match=re.match(r' *(\d{4}-\d{2}-\d{2}) (.*)',kk)
    if(kk_match):
     posts_key.append([kk_match.group(1),kk_match.group(2)])
 return posts_key
################

 
def proc_req_pass():
 pass_name = request.form.get("username") 
 law_match=re.match(r'lzhlaw-([ads])\ *(.*)',pass_name)
 if(law_match):
  if(law_match.group(1)=="a"):
   resu= "add"
   cmd = "/home/fixer/lzh/group0/bin/law "+"/home/fixer/lzh/lzh.dat -a "+law_match.group(2)
  elif(law_match.group(1)=="d"):
   resu= "delete"
  else:
   cmd = "/home/fixer/lzh/group0/bin/law "+"/home/fixer/lzh/lzh.dat -s "+law_match.group(2)
   output=os.popen(cmd)
   resu= output.read()
   resu= re.sub("\n","<br>",resu)
  return resu
   #resu= re.sub(".*:","",resu)
   #resu= re.sub("\*\*\*\*.*","",resu)
   #return resu
   #return "search "
 else: 
  #output=os.popen('/home/fixer/lzh/Emacs/test')
  output=os.popen(EMACAS_PUBLISH)
  resu= output.read()
  #return resu #for debug update project
  return "can not see details"
       
    
def proc_req_record(everyday_file):
 w_pass = request.form.get("passtext")
 w_text = request.form.get("nnn").encode('utf-8') 
 w_add = request.form.get("add")
 time_stamp = "<"+time.strftime("%Y-%m-%d")+">"
 if(w_text != ""):
  if(w_pass == " "):
   with open(everyday_file,'w') as f:
    f.write(w_add)
    f.write(w_text)
    f.write("\n")
    f.write(time_stamp)
    f.write("\n")
    f.close()
   with open(everyday_file,'r') as f:
    re_str= f.read().decode('utf-8').replace("\n",'<br>')
    f.close()
    return re_str
  else:
   return "wrong"
  if(w_pass == "r"):
   with open(everyday_file,'r') as f:
    re_str = f.read().decode('utf-8').replace("\n", '<br>')
    f.close()
    return re_str


def get_dir_filelist(dir):
 filelist= []
 for filename in os.listdir(dir):
  filelist.append(filename.decode('utf-8'))
 return sorted(filelist,reverse=True)

def get_file_content(filepath):
 with open(filepath,'r') as f:
  content=f.read().decode('utf-8').replace("\n",'<br>')
  f.close()
 return content

def get_dir_filelist_and_each_content(dir):
 array_array =[]
 for filename in os.listdir(dir):
  #filepath= os.path.join(dir,filename.decode('gbk'))
  filepath= dir+filename.decode('utf-8')
  filepath= filepath.encode('utf-8')
  mtime = time.strftime('%y-%m-%d',time.localtime(os.path.getmtime(filepath )))
  with open(filepath,'r') as f:
   content = f.read().decode('utf-8').replace("\n",'<br>')
   array_array.append([mtime, filename.decode('utf-8'),content])
 return sorted(array_array,reverse=True)

def category_from_dir(dir):
 array_array_cap =[]
 array_array_todo =[]
 array_array_memo =[]
 array_array_done =[]
 content = []
 cap_in = 0
 todo_in = 0
 memo_in = 0
 done_in = 0
 #=============================
 # array format 
 #=============================
 # [ [time , head ,  content] ]
 # return 3 arrays which is cap/todo/memo
 #+++++++++++++++++++++++++++++
 for filename in os.listdir(dir):
  with open(dir+filename,'r') as f:
   for kk in f.read().decode('utf-8').split("\n"):
    cap_match= re.match(r'.*\*\*\ CAP\ (.*)',kk)
    todo_match= re.match(r'.*\*\*\ TODO\ (.*)',kk)
    memo_match= re.match(r'.*\*\*\ MEMO\ (.*)',kk)
    if(cap_match or todo_match or memo_match ):
     cap_in =0
     todo_in =0
     memo_in =0
    if(cap_match)    :
     cap_in =1
     array_array_cap.append(["","",[]])
     array_array_cap[-1][0] = filename.replace(".org","")
     array_array_cap[-1][1] = cap_match.group(1)
    if(todo_match)   :
     todo_in =1
     array_array_todo.append(["","",[]])
     array_array_todo[-1][0] = filename.replace(".org","")
     array_array_todo[-1][1] = todo_match.group(1)
    if(memo_match)   :
     memo_in =1
     array_array_memo.append(["","",[]])
     array_array_memo[-1][0] = filename.replace(".org","")
     array_array_memo[-1][1] = memo_match.group(1)

    time_match = re.match(r'^<(\d{4}-\d{2}-\d{2})>',kk)
    if(cap_match or todo_match or memo_match ):
     content = [] 
    elif(not time_match):
     content.append(kk)

    # content
    if(cap_in)   : array_array_cap[-1][2] ='<br>'.join(content)
    if(todo_in)  : array_array_todo[-1][2] ='<br>'.join(content)
    if(memo_in)  : array_array_memo[-1][2] ='<br>'.join(content)
   f.close()

 return sorted(array_array_cap,reverse=True), sorted(array_array_todo,reverse=True), sorted(array_array_memo,reverse=True)


def category_to_dir(filepath,which_dir):
 shutil.move(filepath,which_dir)
def remove_file(filepath):
 shutil.move(filepath,which_dir)

# with open(filepath,'r') as f:
#  content=[]
#  for kk in f.read().decode('utf-8').split("\n"):
#   todo_match= re.match(r'.*\*\*\ TODO\ (.*)',kk)
#   if(todo_match):
#    content.append("**"+" DONE "+todo_match.group(1))
#   else:
#    content.append(kk)
#  f.close()
# with open(filepath,'w') as f:
#  f.write("\n".join(content).encode('utf-8'))
#  f.close()
 


####################
# 更新memo的tag
####################
def update_memo_file(result_back) :
 w_text = request.form.get("memo_chk_sta").encode('utf-8') 
 with open(result_back,'w') as f:
  f.write(w_text)
  f.close()
 for kk in w_text.split("\n"):
  head_match=re.match(r'^(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})\ .*(\*\*\*\*last_time.*\*\*\*\*).*',kk)
  has_tag = 0
  if(head_match):
   filename = USERDIR+"capture/everyday/"+head_match.group(1)+".org"
   repl_str= head_match.group(2)
   content= []
   with open(filename,'r') as f:
    for line in f.read().decode('utf-8').split("\n"):
     tag_match=re.match(r'.*(\*\*\*\*last_time.*\*\*\*\*).*',line)
     if(tag_match):
      has_tag = 1
      content.append(repl_str)
     else:
      content.append(line)
    if(not has_tag  ): content.append(repl_str)
   f.close()
   with open(filename,'w') as f:
    f.write("\n".join(content).encode('utf-8'))
   f.close()
 return "record success!"


####################
# 两个整理函数,不是正常routine中的内容.
####################

def split_capture_org():
 i = 10
 content = []
 filename = USERDIR+"capture/input/"+"capture.org"
 with open(filename,'r') as f:
  for kk in f.read().decode('utf-8').split("\n"):
   head_match= re.match(r'^\*\*\ \w*\ (.*)',kk)
   time_match= re.match(r'.*<(\d{4}-\d{2}-\d{2}).*',kk)
   if(head_match) :
    if(i!=10) :
     print i
     with open(pathname,'w') as ff:
      ff.write("\n".join(content).encode('utf-8'))
      ff.close()
    content = []

   content.append(kk)

   if(time_match):
    title = time_match.group(1) +"-00-00-"+str(i)+".org"
    pathname = USERDIR+"capture/input/"+title
    i=i+1
 f.close()

    
def split_everyday_org():
 i = 10
 content = []
 dir = USERDIR+"capture/everyday/"

 for filename in os.listdir(dir):
  filepath=dir+filename
  with open(filepath,'r') as f:
   for kk in f.read().decode('utf-8').split("\n"):
    head_match= re.match(r'^\*\*\ \w*\ (.*)',kk)
    time_match= re.match(r'.*<(\d{4}-\d{2}-\d{2}).*',kk)
    if(head_match) :
     if(i!=10) :
      print i
      with open(pathname,'w') as ff:
       ff.write("\n".join(content).encode('utf-8'))
       ff.close()
     content = []

    content.append(kk)

    if(time_match):
     title = time_match.group(1) +"-00-00-"+str(i)+".org"
     pathname = USERDIR+"capture/tmp/"+title
     i=i+1
  f.close()

