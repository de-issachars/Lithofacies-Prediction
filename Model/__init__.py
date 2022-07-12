
import pickle
import pandas as pd
import numpy as np
import xgboost as xgb



model = xgb.XGBRegressor()
model.load_model('Model/model_lithoPred.json')



#Encoding Categor
def get_prediction_csv(file):
    # file = open(filepath, "r")
    df = pd.read_csv(file, sep =";")
    original_df = df.copy()
    # Encoding Categorical Variables
    df['GROUP_encoded'] = df['GROUP'].astype('category')
    df['GROUP_encoded'] = df['GROUP_encoded'].cat.codes 

    df['FORMATION_encoded'] = df['FORMATION'].astype('category')
    df['FORMATION_encoded'] = df['FORMATION_encoded'].cat.codes

    df['WELL_encoded'] = df['WELL'].astype('category')
    df['WELL_encoded'] = df['WELL_encoded'].cat.codes
    
    #Removing unwanted columns
    df = df.drop([ "RSHA", "SGR", "DCAL", "MUDWEIGHT", "RMIC" , "RXO"],axis=1)
    
    #FILLING MISSING VALUES
    df = df.fillna(-9999)
    
    # dropping the previous columns after encoding
    df = df.drop(['WELL', "GROUP",'FORMATION'], axis=1)
    print(df["WELL_encoded"].unique())
    result = model.predict(df)
    
    result_df = pd.DataFrame(result)
    result_df = result_df.idxmax(axis=1)

    result_df = result_df.to_frame()
    
    result_df.columns = ["LithoPred"]
    conditions = [ (result_df['LithoPred'] == 0), (result_df['LithoPred'] == 1), 
                  (result_df['LithoPred'] == 2),(result_df['LithoPred'] == 3), 
                  (result_df['LithoPred'] == 4),(result_df['LithoPred'] == 5),
                  (result_df['LithoPred'] == 6) , (result_df['LithoPred'] == 7),
                    (result_df['LithoPred'] == 8) , (result_df['LithoPred'] == 9),
                    (result_df['LithoPred'] == 10),(result_df['LithoPred'] == 11)
                    ]
    values = ['Sandstone', 'Sandstone/Shale', 'Shale', 'Marl','Dolomite', 
              'Limestone', 'Chalk', 'Halite','Anhydrite', 'Tuff', 'Coal', 'Basement']
    result_df['PredictedFacies'] = np.select(conditions, values)
    return pd.concat([original_df, result_df], axis=1)
