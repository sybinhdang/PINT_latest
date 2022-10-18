import os

class Input:

    SWAdap_folder = '/Conf/SWAdp/'
    
    SWAdap_X63_folder = '/Conf/SWAdp_X63/'
    
    SWAdap_IO = ["Adc_Report.txt", 
                 "Dio_Report.txt", 
                 "Mcu_Report.txt", 
                 "Port_Report.txt", 
                 "rba_IoExtCj135_ForwardReport.txt", 
                 "rba_IoExtCj135_GenerateReport.txt", 
                 "rba_IoExtCj950_Report.txt",
                 "rba_IoExtCy329_Report.txt", 
                 "rba_IoExtL9959_Report.txt", 
                 "rba_IoExtLib_Report.txt", 
                 "rba_IoMcuAdc_Report.txt",
                 "rba_IoSigAdc_Report.txt", 
                 "Spi_Report.txt"]
    
    EEPROM =   ["NvM_Report.txt", 
                "rba_EepAdaptDGS.h", 
                "rba_EepAdaptDGS_Cfg.c", 
                "rba_EepAdaptDGS_Cfg.h",
                "rba_EepAdaptDGS_Report.txt",
                "rba_EepAdaptDGS_SupplyMem_Cfg.h"]

    def __init__(self, CurrentPVER, PredecessorPVER, PathWorkspace, PathBuilt, PathPredecessor):
        self.CurrentPVER = CurrentPVER              #Name of current PVER
        self.PredecessorPVER = PredecessorPVER      #Name of predecessor PVER
        self.PathWorkspace = PathWorkspace          #Path of Workspace
        self.PathBuilt = PathBuilt                  #Path of current built PVER (BCT + MDGB)
        self.PathPredeccessor = PathPredecessor
        self.readme= "differences exist between current PVER " + CurrentPVER + " and predecessor " + PredecessorPVER
        # Copy swadap
        self.swadp_CurrentPVER = {
            PathBuilt + self.SWAdap_folder : ['swadp.c', 'swadp_confdata.xml', 'swadp_pavast.xml' ],
            PathBuilt + self.SWAdap_X63_folder : ['swadp_x63.c', 'swadp_x63_pavast.xml']
        }



