import pandas as pd
import time
import tqdm

class filter():
    
    def __init__(self, rmv) -> None:
        self.rmv_black_img = rmv

    def remove_black_img(self, data):
        # given an input dataframe, check each image whether maximum value of pixel is 0
        n_removed_img = 0
        filtered_data = pd.DataFrame()
    
        for i, img in enumerate(tqdm.tqdm(data['image'], total=data.shape[0])):
            if img.max() == 0:
                n_removed_img += 1
                continue
            filtered_data = pd.concat([filtered_data, data.iloc[i]], axis=1)
            
        print("Removed {} black images".format(n_removed_img))
        return filtered_data.transpose(), n_removed_img
    
    def apply(self, data):
        if self.rmv_black_img:
            return self.remove_black_img(data)
        
        
def remove_black_img(data):
    # given an input dataframe, check each image whether maximum value of pixel is 0
    n_removed_img = 0
    filtered_data = pd.DataFrame()

    for i, img in enumerate(tqdm.tqdm(data['image'], total=data.shape[0])):
        if img.max() == 0:
            n_removed_img += 1
            continue
        filtered_data = pd.concat([filtered_data, data.iloc[i]], axis=1)
        
        #print("Removed {} black images".format(n_removed_img))
    return filtered_data.transpose(), n_removed_img
