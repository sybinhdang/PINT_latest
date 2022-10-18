import os
import shutil
from filecmp import dircmp
import Common
import time
import text_file as text
from log import logfile

log = logfile('Log_test')

def execute(inputData):
    differentFile = list()
    
    #########################################################################################################################################
    #           3.1_SW_Adapter                                                                                                              #
    #########################################################################################################################################
    log.text(text.banner_3_1)
    time.sleep(0.5)
    ws = inputData.PathWorkspace + "PVER_Conf/3.1_SW_Adapter/"
    ws_pre = inputData.PathPredeccessor + "PVER_Conf/3.1_SW_Adapter/"
    
    #Create current folder 
    log.text('\nCleaning and Creating folder for SWAdp Start...')
    folder = ["_SWAdp\\", "_SWAdp/SWAdp\\", "_SWAdp/SWAdp_X63\\"]
    for i in folder:
        tempFolder = ws + inputData.CurrentPVER + i
        if os.path.exists(tempFolder):
            os.remove(tempFolder)
            log.infor('Delete ' + tempFolder)
        os.mkdir(tempFolder)
        log.infor('Create ' + tempFolder)
    log.text('Cleaning and Creating folder for SWAdp Done')
    
    # tmp = ws + inputData.CurrentPVER  + folder[1]
    
    # Copy swadp file
    i = 1
    log.text('\nCopying SWAdp files form Current PVER Start...')
    try:
        for key in inputData.swadp_CurrentPVER.keys():
            Common.copyFile(ws + inputData.CurrentPVER  + folder[i], key, inputData.swadp_CurrentPVER[key], False)
            log.infor('Copying ' + key)
            i += 1
    except Exception as ex:
        log.error(ex)
    log.text('Copying SWAdp files form Current PVER Done')
    
    log.text('\nCopying SWAdp files form Predecessor PVER Start...')    
    try:
        shutil.copytree(ws_pre + inputData.PredecessorPVER + folder[0], ws + inputData.PredecessorPVER + folder[0])
    except Exception as ex:
        log.warning(ex)
    log.text('Copying SWAdp files form Predecessor PVER Done')
        
    
    #Path of report file after comparing 2 folder
    reportFile = inputData.PathWorkspace + "/Temp/report_compare.txt"
    if os.path.exists(reportFile):
        os.remove(reportFile)
    f = open(reportFile, "w")
    f.close()

    log.text('\nCompare files between Current PVER & Predecessor PVER:') 
    try:
        dcmp = dircmp(ws + inputData.CurrentPVER + folder[0], ws + inputData.PredecessorPVER + folder[0]) 
        Common.compareTwoFolder(dcmp, differentFile)
        Common.readmeFile(len(differentFile), "SWAdp ", ws, inputData.readme)
        log.infor("SWAdp " + inputData.readme)
        differentFile.clear()
    except Exception as ex:
        log.error(ex)
    log.text('Compare Done') 
    
    log.text("\n=================== 3.1: Done")


    #########################################################################################################################################
    #           3.2_IO_Test
    #########################################################################################################################################   
    log.text(text.banner_3_2)
    time.sleep(0.5)
    ws = inputData.PathWorkspace + "PVER_Conf/3.2_IO_Test/"
    ws_pre = inputData.PathPredeccessor + "PVER_Conf/3.2_IO_Test/"

    os.mkdir(ws + inputData.CurrentPVER + "_reports")
    
    # Copy io file
    log.text('\nCopying IO files form Current PVER Start...')
    try:
        Common.copyFile(ws + inputData.CurrentPVER  + "_reports", inputData.PathBuilt + "_out/", inputData.SWAdap_IO, False)
    except Exception as ex:
        log.error(ex)
    log.text('Copying SWAdp files form Current PVER Done')
    
    log.text('\nCopying IO files form Predecessor PVER Start...')
    try:    
        shutil.copytree(ws_pre + inputData.PredecessorPVER + "_reports" , ws + inputData.PredecessorPVER + "_reports")
    except Exception as ex:
        log.warning(ex)
    log.text('Copying SWAdp files form Predecessor PVER Done')

    # Create readme file.
    log.text('\nCompare files between Current PVER & Predecessor PVER:') 
    try:
        dcmp = dircmp(ws + inputData.PredecessorPVER + "_reports", ws + inputData.CurrentPVER + "_reports")  
        Common.compareTwoFolder(dcmp, differentFile)
        Common.readmeFile(len(differentFile), "IO ", ws, inputData.readme)
        log.infor("IO " + inputData.readme)
        differentFile.clear()
    except Exception as ex:
        log.error(ex)
    log.text('Compare Done') 
    
    log.text("\n=================== 3.2: Done")
    
    #########################################################################################################################################
    #           3.3_ECU_Outputs
    #########################################################################################################################################  
    log.text(text.banner_3_3)
    log.text('This step not required, will be skip...')
    #########################################################################################################################################
    #           PVER-F DONE
    #########################################################################################################################################
