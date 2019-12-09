#!/usr/bin/python
# _*_ coding:utf-8 _*_

import re
from flask import request
import os
import time
from vars_common import *



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


#----------------------------
#| 1 | word add          |
#| 2 | word delete       |
#| 3 | word search       |
#| 4 | update emacs html |
#| 5 | tip write         |
#| 6 | tip append        |
#| 7 | tip read          |
#|   |                   |
#|   |                   |
#|   |                   |
#|   |                   |
#|   |                   |
#|   |                   |
#|   |                   |
#|   |                   |
#----------------------------
def proc_req():
    if request.method=='POST' and request.form.get("pass") :
        return 1
    elif request.method=='POST' and request.form.get("passtext") :
        return 2
    elif request.method=='POST' and request.form.get("memo_chk_sta"):
        return 3
    else:
        return 0

 
def proc_req_pass():
    pass_name = request.form.get("pass") 
    law_match=re.match(r'lzhlaw-([ads])\ *(.*)',pass_name)
    if(law_match):
        if(law_match.group(1)=="a"):
            return "add"
        elif(law_match.group(1)=="d"):
            return "delete"
        else:
            cmd = USERDIR+"group0/bin/law "+USERDIR+"/lzh.dat -s "+law_match.group(2)
            output=os.popen(cmd)
            resu= output.read()
            resu= re.sub("\n","",resu)
            resu= re.sub(".*:","",resu)
            resu= re.sub("\*\*\*\*.*","",resu)
            return resu
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
    time_stamp = "<20"+time.strftime("%y-%m-%d")+">"
    if(w_text != ""):
        if(w_pass == " "):
            with open(everyday_file,'w') as f:
                f.write(w_add)
                f.write(w_text)
                f.write("\n")
                f.write(time_stamp)
                f.write("\n")
        elif(w_pass == "a"):
            with open(everyday_file,'a') as f:
                f.write(w_add)
                f.write(w_text)
                f.write("\n")
                f.write(time_stamp)
                f.write("\n")
        if(w_pass == " " or w_pass == "a" or w_pass == "r" ):
            with open(everyday_file,'r') as f:
                return f.read().decode('utf-8')
        else:
            return "wrong !!!"
    if(w_pass == "r"):
        with open(everyday_file,'r') as f:
            return f.read().decode('utf-8')

def proc_to_rem_file(to_rem_file) :
    with open(to_rem_file) as f:
        head=""
        time=""
        grp_tmp=[]
        out_array=[]
        for kk in  f.read().decode('utf-8').split("\n"):
            kk_match= re.match(r'\*\*\*\*(.*)',kk)
            if(kk_match):
                last_head =head
                last_time =time
                head=kk_match.group(1) 
                temp=head

                kk_match=re.match(r'(\d\d\d\d-\d\d-\d\d)\s*(.*)',temp)
                time=kk_match.group(1) if(kk_match) else " "
                head=kk_match.group(2) if(kk_match) else temp
                #print head
                content = '<br>'.join(grp_tmp)
                grp_tmp=[]
                out_array.append([last_time,last_head,content])
            else:
                grp_tmp.append(kk)
                
                
    content = '<br>'.join(grp_tmp)
    out_array.append([time,head,content])
    out_array.pop(0)
    new_arr=sorted(out_array ,reverse=True)
    return new_arr

def back_from_browser(result_back) :
    w_text = request.form.get("memo_chk_sta").encode('utf-8') 
    with open(result_back,'w') as f:
        f.write(w_text)
