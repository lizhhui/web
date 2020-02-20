import os

USERDIR = "/home/fixer/html/"
#USERDIR = "/home/fixer/lzh/web/flask/main/"
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
APP_STATIC_TXT = os.path.join(APP_ROOT, 'static/txt')
BLOG_INDEX = os.path.join(APP_ROOT,"static/html/z_blog/index.html")
BLOG_DIR = USERDIR+"z_blog/"
EMACAS_PUBLISH = USERDIR+'Emacs/emacs_publish.expect'
CAP_PL = 'cd capture ; ./capture_sort.pl input/capture.org'
EVERYDAY_DIR = USERDIR+"capture/everyday/"
ARTICLE = USERDIR+"capture/article/"
REM_FILE= USERDIR+"capture/output/to_rem.html"
TODO_FILE = USERDIR+"capture/output/task.html"
CAP_FILE =  USERDIR+"capture/output/cap.html"
RECORD_BACK= USERDIR+"capture/input/check_status.txt"
