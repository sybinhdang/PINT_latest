import sys
import subprocess
import importlib.util

# subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade','pip'])

# package = ['filecmp', 'time', 'sqlite3', 'pandas', 'argparse', 'shutil', 'datetime', 'sqlalchemy']
# for i in package:
#     if importlib.util.find_spec(i) is None:
#         subprocess.check_call([sys.executable, '-m', 'pip', 'install', i])

import os
import time
import inputData
import PVER_Conf
import PVER_I
import shutil
import argparse
import text_file as text
from log import logfile

class App:
    
    # PVER_Curr       = '90V1004B4B'
    # PVER_Pre        = '90V100496B'
    # Working_Path    = r'C:\Users\DAB5HC\Documents\workspace\SWPD\test_PINT\PINT\4B4B'
    # PVER_Build      = r'C:\Users\DAB5HC\Documents\workspace\SWPD\test_PINT\S68T0_90V1004B4B'
    # PINT_Pre        = r'C:\Users\DAB5HC\Documents\workspace\SWPD\test_PINT\PINT\496B'
    
    # print('\n')
    # print('\n')
    # print(text.banner)
    # print('\n')
    # print('\n')

    log = logfile('Log_test')
    log.create_log()
    
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Script PINT")
    parser.add_argument('--CFG_PATH',required=True, type=str ,help='path to config file')
    args = parser.parse_args()
    text_path = os.path.normpath(args.CFG_PATH)
    
    with open (text_path, 'r', encoding = 'utf-8') as text_file:
        content = text_file.read()
        content = content.replace(" ", "")
        content = content.split('\n')

    log.text(text.banner_start)

    for i in content:  
        elem = i.split('=')
        if 'PVER_Curr' in elem:
            PVER_Curr = elem[-1]
        elif 'PVER_Pre' in elem:
            PVER_Pre = elem[-1]
        elif 'Working_Path' in elem:
            Working_Path = elem[-1]
        elif 'PVER_Build' in elem:
            PVER_Build = elem[-1]
        elif 'PINT_Pre' in elem:
            PINT_Pre = elem[-1]

    temp_path = [ Working_Path, PVER_Build, PINT_Pre]
    flag = 0
    for path in temp_path:
        path = os.path.normpath(path)
        if os.path.exists(path):
            log.infor(" Path {} is exist".format(path))
        else:
            flag = 1
            log.error(" Path {} is not exist".format(path))   
    
    if flag:
        log.error('Path is not correct. Script can not be executed. End')
        log.text(text.banner_done)
    else:
        dataInput = inputData.Input(PVER_Curr, 
                                    PVER_Pre,
                                    os.path.normpath(Working_Path) + '//',
                                    os.path.normpath(PVER_Build) + '//',
                                    os.path.normpath(PINT_Pre) + '//')
        
        log.text('\nCleaning the workspace Start...')
        
        list_dir = os.listdir(dataInput.PathWorkspace)
        for i in list_dir:
            if os.path.isfile(dataInput.PathWorkspace + i):
                os.remove(dataInput.PathWorkspace + i)
                log.infor('Delete ' + i)
            else:
                shutil.rmtree(dataInput.PathWorkspace + i)
                log.infor('Delete ' + i)
        log.text('Cleaning the workspace Done')
        
        Script_dir = os.path.normpath(r'\\bosch.com\dfsrb\DfsIN\loc\cob\NE1\Assorted\EEV_Dept\SRL_LCT\LC_Tests\prg\011\DAB5HC\Tool\PINT')
                    
        time.sleep(0.5)
        
        log.text('\nCreating the workspace Start...')
        subprocess.Popen(Script_dir + '\\Create_ws.bat ' + dataInput.PathWorkspace)
        log.text('Creating the workspace Done')
        
        log.text('\nCopying the check list Start...')
        shutil.copy(Script_dir + '\\gpckCE_TST_PVER-Conf_en.xlsm', dataInput.PathWorkspace)
        shutil.copy(Script_dir + '\\ckSW_PVER_Review_CE.xlsx', dataInput.PathWorkspace)
        log.text('Copying the check list Done')
        
        log.text(text.banner_PVER_conf_start)
        PVER_Conf.execute(dataInput)
        log.text(text.banner_PVER_conf_done)
        
        log.text(text.banner_PVER_I_start)
        PVER_I.execute(dataInput)
        log.text(text.banner_PVER_I_done)
        log.text(text.banner_done)
       

run=App()

