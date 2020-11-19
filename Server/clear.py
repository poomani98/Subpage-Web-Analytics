import pandas as pd
import numpy as np
hm = pd.DataFrame(np.zeros((72,153)))
hm.to_csv("heatmap.csv",index=False,header=False)
