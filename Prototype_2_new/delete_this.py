import pandas as pd

data = pd.read_csv('resources.csv')
x = data.iloc[:,0]
y = x.drop_duplicates()
print(y.to_numpy())
for index, row in data.iterrows():
    class_name = row[0]
    text_name = row[1]
    url = row[2]
    description = "Readings for" + text_name
    print(f"class name: {class_name}, text name: {text_name}, url: {url}, description: {description}")
    