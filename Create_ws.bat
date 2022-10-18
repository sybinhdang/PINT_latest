@REM @RD /s /q *
SET DIR=%1
::SET Temp=%cd%
@REM echo %DIR%
cd /d %DIR% 
SET LIST=Temp PVER_Conf PVER_I PVER_Conf\3.1_SW_Adapter PVER_Conf\3.1_SW_Adapter\_mails PVER_Conf\3.2_IO_Test PVER_Conf\3.2_IO_Test\_mails PVER_Conf\3.3_ECU_Outputs PVER_Conf\3.3_ECU_Outputs\_mails PVER_I\2.1_Software_Analyzer PVER_I\2.1_Software_Analyzer\_mails PVER_I\2.2_Scheduling_Information PVER_I\2.2_Scheduling_Information\_mails PVER_I\2.3_Monitoring_eMFace PVER_I\2.3_Monitoring_eMFace\_mails PVER_I\2.4_Locked_BCs_in_PVER PVER_I\2.4_Locked_BCs_in_PVER\_mails PVER_I\2.5_EEPROM_Report PVER_I\2.5_EEPROM_Report\_mails PVER_I\2.6_Memory_Measurement PVER_I\2.6_Memory_Measurement\_mails PVER_I\2.7_Compiler_Bugs PVER_I\2.7_Compiler_Bugs\_mails PVER_I\2.8_System_Constant_changes PVER_I\2.8_System_Constant_changes\_mails PVER_I\2.9_Memcheck PVER_I\2.9_Memcheck\_mails PVER_I\3.0_Software_complexity_reduction PVER_I\3.0_Software_complexity_reduction\_mails PVER_I\3.1_PVER_Reproducibility PVER_I\3.1_PVER_Reproducibility\_mails PVER_I\3.1_PVER_Reproducibility\before_checkin PVER_I\3.1_PVER_Reproducibility\after_checkin 
 
md %LIST%