import numpy as np
import pandas as pd 
import glob

path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code'
filenames = glob.glob(path + "/WSC Energy*.csv")
dfs = [pd.read_csv(f) for f in filenames]
