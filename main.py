import sys
import subprocess
import importlib.util

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade','pip'])

package = ['filecmp', 'time', 'sqlite3', 'pandas', 'argparse', 'shutil', 'datetime']
for i in package:
    if importlib.util.find_spec(i) is None:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', i])

import os
import time
import inputData
import PVER_Conf
import PVER_I, PVER_I_test_emface
import shutil
import argparse
import text_file as text

class App:
    
    # PVER_Curr = '90V20243LB'
    # PVER_Pre = '90V20243KB'
    # Working_Path = r'C:\Users\DAB5HC\Documents\workspace\SWPD\90V20243LB\PINT\43LB'
    # PVER_Build = r'C:\Users\DAB5HC\Documents\workspace\SWPD\90V20243LB\S68T0_90V20243LB'
    # PINT_Pre = r'C:\Users\DAB5HC\Documents\workspace\SWPD\90V20243LB\PINT\43KB'
    
    print('\n')
    print('\n')
    print(text.banner)
    print('\n')
    print('\n')

    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Script PINT")
    parser.add_argument('--CFG_PATH',required=True, type=str ,help='path to config file')
    args = parser.parse_args()
    text_path = os.path.normpath(args.CFG_PATH)
    
    with open (text_path, 'r', encoding = 'utf-8') as text_file:
        content = text_file.read()
        content = content.replace(" ", "")
        content = content.split('\n')

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

    dataInput = inputData.Input(PVER_Curr, 
                                PVER_Pre,
                                os.path.normpath(Working_Path) + '//',
                                os.path.normpath(PVER_Build) + '//',
                                os.path.normpath(PINT_Pre) + '//')
    
    list_dir = os.listdir(dataInput.PathWorkspace)
    for i in list_dir:
        if os.path.isfile(dataInput.PathWorkspace + i):
            os.remove(dataInput.PathWorkspace + i)
        else:
            shutil.rmtree(dataInput.PathWorkspace + i)
    
    Script_dir = os.path.normpath(r'C:\Users\DAB5HC\Documents\workspace\Tool\Tool_PINT_3')
                
    time.sleep(0.5)
    subprocess.Popen(Script_dir + '\\Create_ws.bat ' + dataInput.PathWorkspace)
    
    shutil.copy(Script_dir + '\\gpckCE_TST_PVER-Conf_en.xlsm', dataInput.PathWorkspace)
    shutil.copy(Script_dir + '\\ckSW_PVER_Review_CE.xlsx', dataInput.PathWorkspace)
    PVER_Conf.execute(dataInput)
    PVER_I.execute(dataInput)
    # PVER_I_test_emface.execute(dataInput)
       

run=App()

"""
----------------------------------------------------------------------------------------------------
2.1_Software_Analyzer
----------------------------------------------------------------------------------------------------
2.2_Scheduling_Information ________ TextLogFiles_CUR
            |
	        |
    TextLogFiles_PRE
----------------------------------------------------------------------------------------------------
2.3_Monitoring_eMFace
----------------------------------------------------------------------------------------------------
2.4_Locked_BCs_in_PVER
----------------------------------------------------------------------------------------------------
2.5_EEPROM_Report  ________ CUR_PVER_report
            |
        	|
    PRE_PVER_report
----------------------------------------------------------------------------------------------------
2.6_Memory_Measurement (N/A)
----------------------------------------------------------------------------------------------------
2.7_Compiler_Bugs (N/A)
----------------------------------------------------------------------------------------------------
2.8_System_Constant_changes
----------------------------------------------------------------------------------------------------
2.9_Memcheck
----------------------------------------------------------------------------------------------------
3.0_Software_complexity_reduction
----------------------------------------------------------------------------------------------------
3.1_PVER_Reproducibility ________ before_checkin
            |
	        |
    after_checkin
----------------------------------------------------------------------------------------------------
"""