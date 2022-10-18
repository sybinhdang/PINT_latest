import os
from datetime import datetime
from pathlib import Path

def Add_version(path_file):
    base_name = os.path.basename(path_file)
    file_name = os.path.splitext(base_name)[0]
    file_type = os.path.splitext(base_name)[-1]
    new_name = file_name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + file_type
    os.rename(path_file, os.path.join(Path(path_file).parent, new_name))
    

