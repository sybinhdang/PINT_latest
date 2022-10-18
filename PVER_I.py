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
import zipfile as zip

Script_dir = os.path.normpath(r'\\bosch.com\dfsrb\DfsIN\loc\cob\NE1\Assorted\EEV_Dept\SRL_LCT\LC_Tests\prg\011\DAB5HC\Tool\PINT')
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
            if msg == 'compare finished successfully':
                return procPID.returncode
                # break
                
        procPID.wait()
        return procPID.returncode

def execute(inputData):
    differentFile = list()
    #########################################################################################################################################
    #           2.1_Software_Analyzer
    #########################################################################################################################################
    log.text(text.banner_2_1)
    log.text('This step will be done manualy...')
    #########################################################################################################################################
    #           2.2_Scheduling_Information
    #########################################################################################################################################
    log.text(text.banner_2_2)
    time.sleep(0.5)
    ws = inputData.PathWorkspace + "PVER_I/2.2_Scheduling_Information/"
    ws_pre = inputData.PathPredeccessor + "PVER_I/2.2_Scheduling_Information/"

    log.text('\nCopying Procman log files form Current PVER Start...')
    try:
        dir1 = inputData.PathBuilt + "_log/ProcMan/"
        if(os.path.exists(dir1)):
            dir1 += os.listdir(dir1)[0] + "/"
            lst_dir2 = os.listdir(dir1)
            dir3 = lst_dir2[-1] + "/TextLogFiles/"
            shutil.copytree(dir1 + dir3, ws + "TextLogFiles_" + inputData.CurrentPVER)
    except Exception as ex:
        log.warning(ex)
    log.text('Copying Procman log files form Current PVER Done')
    
    log.text('\nCopying Procman log files form Predecessor PVER Start...')
    try:
            if os.path.exists(ws_pre + "TextLogFiles_" + inputData.PredecessorPVER):
                shutil.copytree(ws_pre + "TextLogFiles_" + inputData.PredecessorPVER, ws + "TextLogFiles_" + inputData.PredecessorPVER)         
    except Exception as ex:
        log.warning(ex)
    log.text('Copying Procman log files form Predecessor PVER Done')
    
    log.text('\nCompare files between Current PVER & Predecessor PVER:') 
    try:
        dcmp = dircmp(ws + "TextLogFiles_" + inputData.PredecessorPVER, ws + "TextLogFiles_" + inputData.CurrentPVER) 
        Common.compareTwoFolder(dcmp, differentFile)
        Common.readmeFile(len(differentFile), "Scheduling ", ws, inputData.readme)
        log.infor("Scheduling " + inputData.readme)
        differentFile.clear()
    except Exception as ex:
        log.warning(ex)
    log.text('Compare Done') 
    
    log.text("\n=================== 2.2: Done")
    
    #########################################################################################################################################
    #           2.3_Monitoring_eMFace
    #########################################################################################################################################
    log.text(text.banner_2_3)
    time.sleep(0.5)
    ws = inputData.PathWorkspace + "PVER_I/2.3_Monitoring_eMFace/"

    log.text('\nLooking for MO version, will take few mins...')
    try:    
        groovy_path = Script_dir + "\\MO_version_check.groovy"
        
        path = "texec lwscli " + groovy_path + " workUnitPath=" + inputData.PathBuilt
        # print(path)
        
        p = subprocess.Popen(path, stdout=subprocess.PIPE, bufsize=1, text=True, shell=True)
        while p.poll() is None:
            msg = p.stdout.readline().strip()  # read a line from the process output
            if msg:
                if 'Mo_version:' in msg:
                    print("Mo_version: ", msg[msg.index(':')+1:])
                    log.infor('Mo_version: ' + msg[msg.index(':')+1:])
                    Mo_version = msg[msg.index(':')+1:]
                    
                if 'Mo_Revision:' in msg:
                    print("Mo_Revision: ", msg[msg.index(':')+1:])
                    log.infor('Mo_Revision: ' + msg[msg.index(':')+1:])
                    Mo_Revision = msg[msg.index(':')+1:]
    except Exception as ex:
        log.error(ex)  
    log.text('Looking for MO version Done')              
    
    log.text('\nLooking for *.xls file in project path Start...')    
    try:    
        Mo_xls_path = r"\\bosch.com\dfsrb\DfsDE\DIV\DGS\08\EC\58_ESS\PJ\30_Engine_Control_Monitoring\ME_D_Ueberwachung_Konfigurationen\Funktionssoftwarekonfigurationen\Summenkonfigurationen\011_bmw"
        lst_Mo_files = os.listdir(Mo_xls_path)
        log.infor('Number of files in project path: ' + str(len(lst_Mo_files)))

        if "_" in Mo_version:
            Mo_version = Mo_version.replace("_","__")
            Mo_version = Mo_version.replace(".","_")

        case_1 = "SK_" + Mo_version.replace(".","_") + "__" + Mo_Revision
        case_2 = "SK_" + Mo_version.replace(".","_")

        log.text('Name of *.xls file could be {} of {}'.format(case_1, case_2))

        xls_list = []
        SK_files_lst = []
        for file in lst_Mo_files:
            if ".xls" in file:
                xls_list.append(file)
        for file in xls_list:
            if case_1 in file:
                SK_files_lst.append(file)
            elif case_2 in file:
                SK_files_lst.append(file)

        log.infor('Found ' + str(len(SK_files_lst)) + ' file: ' + str(SK_files_lst))
        
    except Exception as ex:
        # xls_list = []
        # SK_files_lst = []
        log.error(ex)
    log.text('Looking for *.xls file in project path Done') 
            
        
    # if (SK_files_lst != null):
    if (len(SK_files_lst) != 0):
        SK_file = SK_files_lst[-1]
        log.infor('File been found: ' + SK_file)
        try:
            log.text("\nCopy and Modify emface_BMW.bat script Start...")
            if os.path.isfile(inputData.PathBuilt + "\\emface_BMW.bat"):
                    os.remove(inputData.PathBuilt + "\\emface_BMW.bat")
            shutil.copyfile(Script_dir + "\\emface_BMW.bat", inputData.PathBuilt + "\\emface_BMW.bat")
            log.text('\nModify ')
            emface_file = open(inputData.PathBuilt + "emface_BMW.bat","r")
            ori_path = "SK_11_39_27.xls"
            content = emface_file.read()
            new_content = content.replace(ori_path, SK_file)
            emface_file = open(inputData.PathBuilt + "emface_BMW.bat","w")
            emface_file.write(new_content)
            emface_file.close()
            log.text("\nCopy and Modify emface_BMW.bat script Done")
            log.text("\nRunning emface_BMW.bat script, will be take approximate 30 mins...")
            cwd = Script_dir
            os.chdir(inputData.PathBuilt)
            emface_run = subprocess.Popen(inputData.PathBuilt + "\\emface_BMW.bat", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            emface_run.communicate(input='<<< Skip Enter >>>'.encode())[0]
            emface_run.wait()
            os.chdir(cwd)
            log.text("Running emface_BMW.bat script Done")
            log.text('\nCopy eMFace output...')
            lst_dir = os.listdir(inputData.PathBuilt)
            emface_rp_lst = []
            for file in lst_dir:
                if "emface_report_4.3.0_mdgb" in file:
                    emface_rp_lst.append(file)
            emface_lst_file = ["makefile.log", "makefile.ulf", "PROCLIST_MDG1_BMW_TUE2_02.txt.pre", emface_rp_lst[-1]]
            # print(emface_lst_file) 
            Common.copyFile(ws, inputData.PathBuilt, emface_lst_file, True)
        except Exception as ex:
            log.error(ex)
    else:
        log.warning('File not found, eMFace script can not be executed')

    
    # try:
    #     log.text('\nCopy eMFace output...')
    #     lst_dir = os.listdir(inputData.PathBuilt)
    #     emface_rp_lst = []
    #     for file in lst_dir:
    #         if "emface_report_4.3.0_mdgb" in file:
    #             emface_rp_lst.append(file)
                
    #     emface_lst_file = ["makefile.log", "makefile.ulf", "PROCLIST_MDG1_BMW_TUE2_02.txt.pre", emface_rp_lst[-1]]
    #     # print(emface_lst_file) 
    #     Common.copyFile(ws, inputData.PathBuilt, emface_lst_file, True)
    # except Exception as ex:
    #     log.error(ex)
    
    log.text("\n=================== 2.3: Done")   
    
    
    #########################################################################################################################################
    #           2.4_Locked_BCs_in_PVER
    #########################################################################################################################################
    log.text(text.banner_2_4)
    log.text('This step have to do manually, will be skip...')
    #########################################################################################################################################
    #           2.5_EEPROM_Report
    #########################################################################################################################################
    log.text(text.banner_2_5)
    time.sleep(0.5)
    ws = inputData.PathWorkspace + "PVER_I/2.5_EEPROM_Report/"
    ws_pre = inputData.PathPredeccessor + "PVER_I/2.5_EEPROM_Report/"
    os.mkdir(ws + inputData.CurrentPVER + "_reports")    
    
    log.text('\nCopying EEPROM files form Current PVER Start...')
    try:
        Common.copyFile(ws + inputData.CurrentPVER  + "_reports", inputData.PathBuilt + "_out/", inputData.EEPROM, False)
    except Exception as ex:
        log.warning(ex)
    log.text('Copying EEPROM files form Current PVER Done')
          
    log.text('\nCopying EEPROM files form Predecessor PVER Start...')
    try:    
        shutil.copytree(ws_pre + inputData.PredecessorPVER + "_reports" , ws + inputData.PredecessorPVER + "_reports")
    except Exception as ex:
        log.warning(ex)
    log.text('Copying EEPROM files form Predecessor PVER Done')
    
    log.text('\nCompare files between Current PVER & Predecessor PVER:')         
    try:    
        dcmp = dircmp(ws + inputData.PredecessorPVER + "_reports", ws + inputData.CurrentPVER  + "_reports") 
        Common.compareTwoFolder(dcmp, differentFile)
        Common.readmeFile(len(differentFile), "Eeprom ", ws, inputData.readme)
        log.infor("Eeprom " + inputData.readme)
        differentFile.clear()
    except Exception as ex:
        log.error(ex)
    log.text('Compare Done') 
    
    log.text("\n=================== 2.5: Done")
    
    #########################################################################################################################################
    #           2.6_Memory_Measuremen
    #########################################################################################################################################
    log.text(text.banner_2_6)
    log.text('This step not required, will be skip...')
    #########################################################################################################################################
    #           2.7_Compiler_Bugs
    #########################################################################################################################################
    log.text(text.banner_2_7)
    time.sleep(0.5)
    ws = inputData.PathWorkspace + "PVER_I/2.7_Compiler_Bugs"
    
    log.text('\nSearching Bug Scan Compiler Version...')
    try:
        config = {}
        with open(inputData.PathBuilt + "/_log/swb/tool_vers.log") as ini_file:
            for line in ini_file:
                if line.startswith('-') or line.startswith('\n') or line.startswith('#') or line.startswith('Tools used'):
                    continue
                key, val = line.strip().split(': ')
                key = key.strip()
                config[key] = val
        compiler_version = config['compiler 1']
        log.infor('Compiler Bug Scanner Version: ' + compiler_version)
        
        if compiler_version == 'c:\toolbase\hightec_ifx\cd_v4.6.6.1-bosch-1.3':
            log.text('\nInit and run mdgb Start...')
            try:
                tini_cmd = "tbcon.cmd " + inputData.PathBuilt + " /app /run:\"tini mdgb -setExtAlias:compiler_1=hightec_ifx/cd_v4.6.6.1-bosch-1.3"
                tini = runCommand(tini_cmd)

                mdgb_cmd = "tbcon.cmd " + inputData.PathBuilt + " /app /run:\"mdgb -r --to=build"
                mdgb = runCommand(mdgb_cmd)
                
            except Exception as ex:
                log.error(ex)
            log.text('Init and run mdgb Done')

            log.text('\nCompiler Bug Scanner Start...')
            try:
                if os.path.exists(inputData.PathBuilt + '\DPPBLM_43_BUGSCAN_SCRIPT.zip'):
                    pass
                else:
                    copy('DPPBLM_43_BUGSCAN_SCRIPT.zip', inputData.PathBuilt)

                with zip.ZipFile(inputData.PathBuilt + "\DPPBLM_43_BUGSCAN_SCRIPT.zip", 'r') as dsq_msg_check:
                            dsq_msg_check.extractall(inputData.PathBuilt)

                install_cmd = "tbcon.cmd " + inputData.PathBuilt + " /app /run:\"installBugFixCompilerVersion.bat"
                install = runCommand(install_cmd)

                bug_scanner_cmd = "tbcon.cmd " + inputData.PathBuilt + " /app /run:\"Bugscanner_DPPBLM-43.bat"
                bug_scanner = runCommand(bug_scanner_cmd)

                if(os.path.exists(inputData.PathBuilt + '\DPPBLM_43_report.txt')):
                    copy(inputData.PathBuilt + '\DPPBLM_43_report.txt', ws)

                with open(inputData.PathBuilt + '\DPPBLM_43_report.txt', 'r') as report:
                    content = report.readlines()
                
                for i in content:
                    i = i.replace('\n','')
                    log.infor(i)
                    
                log.text('Compiler Bug Scanner Done')
                
            except Exception as ex:
                log.error(ex)
        else:
            log.infor('Compiler Bug Scanner Version not required perform Bug Impact Analysis')
    except Exception as ex:
        log.error(ex)
    
    log.text("\n=================== 2.7: Done")
    
    #########################################################################################################################################
    #           2.8_System_Constant_changes
    #########################################################################################################################################
    log.text(text.banner_2_8)
    log.text('This step have to do manually, will be skip...')
    #########################################################################################################################################
    #           2.9_Memcheck
    #########################################################################################################################################
    log.text(text.banner_2_9)
    time.sleep(0.5)  
    ws = inputData.PathWorkspace + "PVER_I/2.9_Memcheck/"
    ws_pre = inputData.PathPredeccessor + "PVER_I/2.9_Memcheck/"
    
    try:
        if os.path.isfile(inputData.PathBuilt + r"\perlhash.pl"):
            log.infor('Found perlhash.pl file')
            shutil.copy(inputData.PathBuilt + r"\perlhash.pl", ws)
        else:
            log.warning('Not found perlhash.pl file')
    except Exception as ex:
        log.warning(ex)
    
    log.text('\nCopying eMFace files and Predecessor report Start...')
    try:        
        shutil.copy(Script_dir + r'\MemCheck_v1.9.pl', ws)
        shutil.copy(Script_dir + r'\MemCheck_v1.9.xlsm', ws)
        shutil.copy(ws_pre + "\\Memcheck_" + inputData.PredecessorPVER + ".xlsm", ws)
    except Exception as ex:
        log.warning(ex)
    log.text('Copying eMFace files and Predecessor report Done')
        
    log.text("\n=================== 2.9: Done")
    
    #########################################################################################################################################
    #           3.0_Software_complexity_reduction
    #########################################################################################################################################
    log.text(text.banner_3_0)
    log.text('This step have to do manually, will be skip...')
    #########################################################################################################################################
    #           3.1_PVER_Reproducibility
    #########################################################################################################################################
    log.text(text.banner_3_1)
    time.sleep(0.5)  
    ws = inputData.PathWorkspace + "PVER_I/3.1_PVER_Reproducibility/"
    
    log.text('\nCopying hex and a2l Start...')
    try:
        lst_dir = os.listdir(inputData.PathBuilt + r"/_bin/swb/")
        file_lst = []
        hex_file = inputData.CurrentPVER + ".hex"
        for file in lst_dir:
            if hex_file in file:
                file_lst.append(file)
        
        shutil.copy(inputData.PathBuilt + r"/_bin/swb/" + file_lst[0], ws + r"/before_checkin/")
        shutil.copy(inputData.PathBuilt + r"/_bin/swb/" + inputData.CurrentPVER + ".a2l", ws + r"/before_checkin/")
    except Exception as ex:
        log.warning(ex)
    log.text('Copying hex and a2l Done for before checkin, after check have to be done manually')
    
    log.text("\n=================== 3.1: Done")
    
    #########################################################################################################################################
    #           PVER-I DONE
    #########################################################################################################################################
    