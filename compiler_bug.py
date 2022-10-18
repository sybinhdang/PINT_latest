import os
import shutil
import subprocess
from filecmp import dircmp
from sqlalchemy import null
import Common
import inputData
import time
import text_file as text
from log import logfile

Script_dir = os.path.normpath(r'C:\Users\DAB5HC\Documents\workspace\Tool\Tool_PINT_3')
log = logfile('Log_test')
    
def copy(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    shutil.copyfile(src, dst)
    
def runCommand(command):
        #return 0
        print("Run command: ", command)
        print("Run command: {}\n".format(command))
        procPID = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, text=True, shell=True)
        while procPID.poll() is None:
            msg = procPID.stdout.readline().strip()  # read a line from the process output
            if msg:
                # If cancel or exit is call -> stop Build
                print(msg + "\n")
        procPID.wait()
        return procPID.returncode
    
def execute(inputData):
    differentFile = list()
    time.sleep(0.5)
    ws = inputData.PathWorkspace + "PVER_I/2.7_Compiler_Bugs"
    
    tini_cmd = "tbcon.cmd " + inputData.PathBuilt + " /app /run:\"tini mdgb -setExtAlias:compiler_1=hightec_ifx/cd_v4.6.6.1-bosch-1.3"
    
    mdgb_cmd = "tbcon.cmd " + inputData.PathBuilt + " /app /run:\"mdgb -r"
    
    runCommand(tini_cmd)
    
    runCommand(mdgb_cmd)
    
    
    