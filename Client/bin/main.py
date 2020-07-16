import os
import sys

# 将Client目录加入Python环境中，以便包导入
BASE_DIR = os.path.dirname(os.getcwd())
sys.path.append(BASE_DIR)

from core import handler

if __name__ == "__main__":
    handler.ArgvHandler(sys.argv)
