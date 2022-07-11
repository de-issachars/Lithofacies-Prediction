from Model import get_prediction_csv

with open("Data/CSV_test.csv", "rb") as csv:
    print(get_prediction_csv(csv))
