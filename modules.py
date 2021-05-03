import re
from pathlib import Path
import os
import shutil
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtWidgets
from main_v2 import Dialog

fp = "c:\\Users\\PRA\\"
files = Path("c:\\Users\\PRA\\")


def removeHistory(filePath):
    for file in filePath.iterdir():
        new_folder_name = re.sub("history_[0-9][0-9][0-9][0-9].", "", file.name)
        file.rename(str(filePath)+"\\"+new_folder_name)


def checkFolderStructure(filePath):
    for file in filePath.iterdir():
        if "Sub" in file.name:
            QtWidgets.QMessageBox.information(Dialog(), "Folder error",
                                              "Folder structure incorrect, "
                                              "make sure sub folder is inside another folder")


def moveLPFolder(fp):
    for folder in os.listdir(fp):
        for sub in os.listdir(fp+folder):
            for task in os.listdir(fp+folder+"\\"+sub):
                if len(os.listdir(fp+folder+"\\"+sub)) > 1:
                    for lp_folder in os.listdir(fp+folder+"\\"+sub+"\\"+task+" ("+str(len(os.listdir(fp+folder+"\\"+sub))-1)+")"):
                        os.rename(os.path.join(fp+folder+"\\"+sub+"\\"+task+" ("+str(len(os.listdir(fp+folder+"\\"+sub))-1)+")\\"+lp_folder),
                                  os.path.join(fp+folder+"\\"+sub+"\\"+lp_folder))
                    break
                else:
                    for lp_folder in os.listdir(fp+folder+"\\"+sub+"\\"+task):
                        os.rename(os.path.join(fp+folder+"\\"+sub+"\\"+task+"\\"+lp_folder), os.path.join(fp+folder+"\\"+sub+"\\"+lp_folder))


def removePdGibberish(filePath):
    for txlf in filePath.glob("**/*.txlf"):
        txlf_name = re.split("(MS Word|-Non-Parsable-)", str(txlf))[0] + txlf.suffix
        txlf.rename(txlf_name,)


def folderDestroyer(fp):
    for folder in os.listdir(fp):
        for sub in os.listdir(fp+folder):
            for shred_me in os.listdir(fp+folder+"//"+sub+"//"):
                if os.path.isdir(fp+folder+"//"+sub+"//"+shred_me):
                    shutil.rmtree(fp+folder+"//"+sub+"//"+shred_me, ignore_errors=True)


def extractTXLF(fp):
    for folder in os.listdir(fp):
        for sub in os.listdir(fp+folder):
            for lp in os.listdir(fp+folder+"//"+sub):
                if "upload" in lp:
                    continue
                else:
                    for txlf in os.listdir(fp+folder+"//"+sub+"//"+lp):
                        os.rename(os.path.join(fp+folder+"//"+sub+"//"+lp+"//"+txlf),
                                  os.path.join(fp+folder+"//"+sub+"//"+txlf))


def renameTXLF(fp):
    for folder in os.listdir(fp):
        for sub in os.listdir(fp+folder):
            for txlf in os.listdir(fp+folder+"/"+sub):
                f = open(fp+folder+"/"+sub+"/"+txlf, encoding="utf-8")
                first_line = f.readline()
                if "target-language" in first_line:
                    target_lp = re.findall('target-language="..-.."', first_line)[0]
                    target_lp = re.sub('target-language="', '', target_lp)
                    target_lp = re.sub('"', "", target_lp)
                    source_lp = re.findall('source-language="..-.."', first_line)[0]
                    source_lp = re.sub('source-language="', '', source_lp)
                    source_lp = re.sub('"', "", source_lp)
                f.close()
                file_name = re.split(".txlf",txlf)[0]
                new_name = sub + "_" + file_name + "_" + source_lp + "_" + target_lp + ".txlf"
                os.rename(os.path.join(fp+folder+"/"+sub+"/"+txlf),
                          os.path.join(fp+folder+"/"+new_name))


def destroySubFolders(fp):
    for folder in os.listdir(fp):
        for file in os.listdir(fp+folder):
            if os.path.isdir(fp+folder+"/"+file):
                shutil.rmtree(fp+folder+"/"+file)

def createTargetFolders(fp):
    target_lp_list = []
    for folder in os.listdir(fp):
        for txlf in os.listdir(fp+folder):
            target_folder = re.findall("[a-z][a-z]-[A-Z][A-Z]_[a-z][a-z]-[A-Z][A-Z].txlf", txlf)[0]
            # target_folder = re.sub("_", "", target_folder)
            target_folder = re.sub(".txlf", "", target_folder)
            target_lp_list.append(target_folder)
            target_lp_list = list(set(target_lp_list))
        for lp in target_lp_list:
            os.mkdir(fp+folder+"/"+lp)


def moveTXLFtoTargetFolders(fp):
    for folder in os.listdir(fp):
        for txlf in os.listdir(fp+folder):
            if ".txlf" in txlf:
                target_folder = re.findall("[a-z][a-z]-[A-Z][A-Z]_[a-z][a-z]-[A-Z][A-Z].txlf",txlf)[0]
                target_folder = re.sub(".txlf", "", target_folder)
                os.rename(os.path.join(fp+folder+"/"+txlf),
                          os.path.join(fp+folder+"/"+target_folder+"/"+txlf))

