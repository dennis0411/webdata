import pandas as pd
import numpy as np
import morningstar
import cnyes
import time

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

if __name__ == '__main__':
    start = time.time()
    C = cnyes.cnyes_source()
    C.return_data()
    c = C.news_data
    M = morningstar.morningstar_report()
    M.return_data()
    m = M.news_data
    data = pd.concat([c, m], ignore_index=True)
    print(data)
    end = time.time()
    print(f'total time: {end - start} seconds')
