import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load

# Read cleaned data into dataframe
pcos_clean_data = pd.read_csv('data/clean_pcos_dataset.csv', sep=';')
print('Raw data shape:', pcos_clean_data.shape)

# Get the inputs (and scale them) and outputs
x = pcos_clean_data[['Cycle(R/I)', 'Weight gain(Y/N)', 'hair growth(Y/N)', 'Skin darkening (Y/N)', 'Pimples(Y/N)', 'Fast food (Y/N)', 'Follicle No. (L)', 'Follicle No. (R)']]
print('Chosen data shape:', x.shape)

inputs = pcos_clean_data[['Cycle(R/I)', 'Weight gain(Y/N)', 'hair growth(Y/N)', 'Skin darkening (Y/N)', 'Pimples(Y/N)', 'Fast food (Y/N)', 'Follicle No. (L)', 'Follicle No. (R)']].values
outputs = pcos_clean_data['PCOS (Y/N)'].values

# Load classifier with best parameters (previously found) and with a maximum number of iterations
decTree = DecisionTreeClassifier(criterion='gini', max_depth=15, max_features='sqrt', splitter='random')

# Since we already have assessed the performance of LinearSVC with the data, we do not need to split the data into train and test sets = let's just train! ;)
decTree.fit(inputs, outputs)

# Serialize model and save for inference later
ser = dump(decTree, 'model/pcos_dtree.joblib')

print('Train finished!')

# Test model on training data
decTree = load('model/pcos_dtree.joblib')

res = decTree.predict(inputs)

count_errors = 0
n_samples = len(res)
for i in range(0, len(res)):
	if res[i] != outputs[i]:
		count_errors += 1

print('Accuracy on training data = ' + str(round((1 - count_errors/n_samples) * 100, 2)) + '%')

