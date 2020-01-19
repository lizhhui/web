import os

#USERDIR = "/Users/lizhanghui/lzh/"
USERDIR = "/home/fixer/lzh/"
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
APP_STATIC_TXT = os.path.join(APP_ROOT, 'static/txt')
BLOG_INDEX = os.path.join(APP_ROOT,"static/html/z_blog/index.html")
EMACAS_PUBLISH = USERDIR+'Emacs/emacs_publish.expect'
CAP_PL = 'cd capture ; ./capture_sort.pl input/capture.org'
Z_BLOG = USERDIR+"emacs/capture/everyday/"
REM_FILE= USERDIR+"emacs/capture/output/to_rem.html"
TODO_FILE = USERDIR+"emacs/capture/output/task.html"
CAP_FILE =  USERDIR+"emacs/capture/output/cap.html"
RECORD_BACK= USERDIR+"emacs/capture/input/check_status.txt"
