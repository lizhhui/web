import os

#USERDIR = "/Users/lizhanghui/lzh/"
USERDIR = "/home/fixer/lzh/"
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
APP_STATIC_TXT = os.path.join(APP_ROOT, 'static/txt')
BLOG_INDEX = os.path.join(APP_ROOT,"static/z_frontPage/index.html")
EMACAS_PUBLISH = USERDIR+'Emacs/emacs_publish.expect'
Z_BLOG = USERDIR+"memos/everyday/"
REM_FILE= USERDIR+"memos/to_rem.html"
TODO_FILE = USERDIR+"memos/task.html"
CAP_FILE =  USERDIR+"memos/cap.html"
RECORD_BACK= USERDIR+"memos/check_status.txt"
