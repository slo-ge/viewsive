import os
import sys
from subprocess import Popen


def main():
    env = os.environ
    if "--debug" in sys.argv:
        env["CEFPYTHON_PYINSTALLER_DEBUG"] = "1"
    sub = Popen(["pyinstaller", "--clean", "start.spec"], env=env)
    sub.communicate()


if __name__ == '__main__':
    main()
