import os
import shutil
import filecmp


Script_dir = os.path.normpath(r'C:\Users\DAB5HC\Documents\workspace\Tool\Tool_PINT_3')

#Create readme file.
def readmeFile(leng, content, path, readme):                    #Create readme file.
    f = open(path + "readme.txt", "w")
    if leng > 0:
        f.write(content + readme)
    else:
        f.write("No " + content + readme)
    f.close()

#Copy file
def copyFile(outputPah, Path, listFile, isTrue):
    if isTrue:
        for f in listFile:
            if os.path.exists(Path  + f):
                shutil.copyfile(Path  + f, outputPah + "/" + f)
    else:
        for f in listFile:
            shutil.copyfile(Path  + f, outputPah + "/" + f)

def createScriptFile(pathfolder1, pathfolder2, wsTemp):
    currentWorkPath = Script_dir
    content = "criteria rules-base\n"
    content += "filter \"*.c;*.xml\"\n"
    content += "load " + pathfolder1 + " " + pathfolder2+ "\n"
    content += "expand all\n"
    content += "folder-report layout:side-by-side options:display-mismatches output-to:" + wsTemp + "/Temp/report_compare.txt"
    
    scriptFile = open(wsTemp + "/Temp/Script.txt", "w")
    scriptFile.write(content)
    scriptFile.close()
    return wsTemp + "/Temp/Script.txt"

# Compare 2 folder
def compareTwoFolder(dcmp, differentFile):
    for name in dcmp.diff_files:
        differentFile.append(name)
    for sub_dcmp in dcmp.subdirs.values():
        compareTwoFolder(sub_dcmp, differentFile)

# Copy folder
# shutil.copytree(ws_pre + inputData.PredecessorPVER + folder[0], ws + inputData.PredecessorPVER + folder[0])