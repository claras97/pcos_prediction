import pandas as pd

pcos_clean_data = pd.read_csv('data/clean_pcos_dataset.csv', sep=';', decimal='.')

selected_pcos_data = pcos_clean_data[['PCOS (Y/N)', 'Follicle No. (L)', 'Weight (Kg)', 'Skin darkening (Y/N)', 'Vit D3 (ng/mL)', 'Pimples(Y/N)', 'Cycle(R/I)', 'Fast food (Y/N)', 'AMH(ng/mL)', 'hair growth(Y/N)', 'Weight gain(Y/N)', 'Cycle length(days)', 'Follicle No. (R)', 'Hair loss(Y/N)', 'Reg.Exercise(Y/N)', 'BMI']]

pcos_values = selected_pcos_data['PCOS (Y/N)'].values

pcos_yes = []
pcos_no  = []

for i in range(0, len(pcos_values)):
	val = pcos_values[i]
	if val == 0:
		pcos_no.append(i)
	elif val == 1:
		pcos_yes.append(i)
	else:
		print("Error: Value should be 0 or 1!")

print('YES = ' + str(len(pcos_yes)) + ' ; NO = ' + str(len(pcos_no)) + '; TOTAL = ' + str(len(pcos_yes) + len(pcos_no)))


pcos_data_yes = selected_pcos_data.drop(index=pcos_no, inplace=False)
pcos_data_yes.drop(columns='PCOS (Y/N)', inplace=True)
#print(pcos_data_yes.head)
pcos_data_yes_desc = pcos_data_yes.describe()
print(pcos_data_yes_desc)
pcos_data_yes_desc.to_csv('data/YES_pcos_data_description.csv', sep=';')

pcos_data_no = selected_pcos_data.drop(index=pcos_yes, inplace=False)
pcos_data_no.drop(columns='PCOS (Y/N)', inplace=True)
#print(pcos_data_no.head)
pcos_data_no_desc = pcos_data_no.describe()
print(pcos_data_no_desc)
pcos_data_no_desc.to_csv('data/NO_pcos_data_description.csv', sep=';')


