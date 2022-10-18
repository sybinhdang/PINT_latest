from Add_version import Add_version
from datetime import datetime
import os
import text_file as text

class logfile:
    
    def __init__(self, log_name):
        self.log_name = log_name
        log_file = os.path.join(os.getcwd(), self.log_name + '.log')
        self.log_file = log_file
        self.time = datetime.now().strftime("%H:%M:%S")
        pass
    
    def create_log(self):
        
        if (os.path.exists(self.log_file)):
            # Add_version(self.log_file)
            os.remove(self.log_file)
            
        with open(self.log_file, 'a', encoding = 'utf-8') as f:
            
            f.write('********************************************************************************************\n')
            f.write('* PINT Tool - V1.0 - Oct.10.2022                                                           *\n')
            f.write('* If there any problem, please contact: Dang Sy Binh (MS/EEU12-PS) - DAB5HC                *\n')    
            f.write('* Find Guideline at link:                                                                  *\n')
            f.write('********************************************************************************************\n')          
            f.write('\n')
            f.write('\n')
            
            f.write(text.banner)
            f.write('\n')
            f.write('\n')
            
            f.write('Creation user: ' + os.getlogin() + '\n')
            f.writelines('Creation date: ' + datetime.now().strftime("%d/%b/%Y %H:%M:%S") + '\n')
            f.write('\n')
            f.write('\n')
            
    def text(self, message):
        with open(self.log_file, 'a', encoding = 'utf-8') as f:
            f.write(message + '\n')
                    
    def infor(self, message):
        with open(self.log_file, 'a', encoding = 'utf-8') as f:
            f.write("{:10}{}\t{}\n".format('INFO', self.time, message))
            
    def warning(self, message):
        with open(self.log_file, 'a', encoding = 'utf-8') as f:
            f.write("{:10}{}\t{}\n".format('WARNING', self.time, message))
            
    def error(self, message):
        with open(self.log_file, 'a', encoding = 'utf-8') as f:
            f.write("{:10}{}\t{}\n".format('ERROR', self.time, message))
    
            
            

run = logfile('Log_test')
run.create_log()
run.text('This is a message !')
run.infor('This is a message !')
run.warning('This is a message !')
run.error('This is a message !')
# run.text(test2.banner)
