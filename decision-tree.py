import sys
import csv
import math
import random


Class_Label = 'ReviewCount'
class CNode:
	left , right, data, seq_Att, seq_Feature, mean_T = None, None, None, None, None, None
	def __init__(self, data):
		self.left = None
		self.right = None
		self.data = data
		self.mean_T = None
		self.seq_Att = None
		self.seq_Feature = None

def BuildTree(node):
	Label_Index = node.data[0].index(Class_Label)
	if len(node.data) == 2:
		node.mean_T = node.data[1][Label_Index]
		#print node.mean_T
		return 

	if len(node.data[0]) == 1:
		node.mean_T = 0
		for row in node.data[1:]:
			node.mean_T += int(row[Label_Index])
		node.mean_T = float(node.mean_T)/(len(node.data) -1)
		#print node.mean_T
		return

	Max_score = 0
	Target_attribute = 0
	Target_Feature = ''
	left = list()
	right = list()

	Sum_X = 0
	Sum_X2 = 0
	for row in node.data[1:]:
		Sum_X += int(row[Label_Index])
		Sum_X2 += int(row[Label_Index])*int(row[Label_Index])

	Ex = float(Sum_X)/(len(node.data)-1)
	Ex2 = float(Sum_X2)/(len(node.data)-1)

	Err = Ex2 - Ex*Ex
	
	col = 0
	while col < len(node.data[0]):
		if col == Label_Index:
			col += 1
			continue
		feature_set = set([row[col] for row in node.data[1:]])
		
		#Preprocess the data calculate Sum_X of Class_label in respect to each feature, 
		#and store them into the dictionary.

		#Initialize the dictionary.
		dictionary_X = {}
		dictionary_X2 = {}
		for feature in feature_set:
			dictionary_X[feature] = 0
			dictionary_X2[feature] = 0

		for row in node.data[1:]:
			dictionary_X[row[col]] += int(row[Label_Index])
			dictionary_X2[row[col]] += int(row[Label_Index])*int(row[Label_Index])

		#Using the dictionary to calculate Scoring function.
		#The Scoring function is S(X,T) = Err(T) - SUM(Pj * Err(Tj))

		for feature in feature_set:
			num_feature = [row[col] for row in node.data[1:]].count(feature)
			num_non_feature = len(node.data) - 1 - num_feature
			P_left = float(num_feature)/(len(node.data)-1)
			P_right = 1 - P_left
			Err_left = float(dictionary_X2[feature])/num_feature - float(dictionary_X[feature])/num_feature*float(dictionary_X[feature])/num_feature
			if num_non_feature == 0:
				Err_right = 0
			else:	
				Err_right = float(Sum_X2-dictionary_X2[feature])/num_non_feature - float(Sum_X-dictionary_X[feature])/num_non_feature*float(Sum_X-dictionary_X[feature])/num_non_feature
			Score = Err - P_left*Err_left - P_right*Err_right

			if Score > Max_score:
				Max_score = Score
				Target_attribute = col
				Target_Feature = feature

		col += 1


	if Max_score <= .25:
		#Calculate the mean of current means of ReviewCount of the data set
		Sum_T = 0
		for row in node.data[1:]:
			Sum_T += int(row[Label_Index])
		node.mean_T = float(Sum_T)/(len(node.data) - 1)
		#print node.mean_T
		return  


	left.append(list(node.data[0]))
	right.append(list(node.data[0]))
	for row in node.data[1:]:
		if row[Target_attribute] == Target_Feature:
			left.append(list(row))
		else:
			right.append(list(row))
	
	for row in left:
		row.pop(Target_attribute)

	#print node.data[0][Target_attribute] +'  '+Target_Feature
	#print Max_score

	node.left = CNode(left)
	BuildTree(node.left)	
	node.right = CNode(right)
	BuildTree(node.right)

	node.seq_Att = node.data[0][Target_attribute]
	node.seq_Feature = Target_Feature





def square_loss(header, row, root):
	Label_Index = header.index(Class_Label)
	while root.seq_Feature != None:
		if row[header.index(root.seq_Att)] == root.seq_Feature:
			root = root.left
		else:
			root = root.right
	#print root.mean_T
	return (int(row[Label_Index]) - int(root.mean_T))*(int(row[Label_Index]) - int(root.mean_T))







if __name__ == "__main__":
	reader = csv.reader(file(sys.argv[1],'rU'))
	train_set = list(reader)

	reader = csv.reader(file(sys.argv[2],'rU'))
	test_set = list(reader)
	
	if 'Longitude' in train_set[0]:
		t = train_set[0].index('Longitude')
		temp = list([row[t] for row in train_set[1:]])
		temp = map(float, temp)
		temp.sort()
		upper = temp[len(temp)/4]
		lower = temp[len(temp)*3/4]
		for row in train_set[1:]:
			row[t] = float(row[t])
			if row[t] <= upper:
				row[t] = 'low'
			elif row[t] >= lower:
				row[t] = 'high'
			else:
				row[t] = 'med'

	if 'Latitude' in train_set[0]:
		t = train_set[0].index('Latitude')
		temp = list([row[t] for row in train_set[1:]])
		temp = map(float, temp)
		temp.sort()
		upper = temp[len(temp)/4]
		lower = temp[len(temp)*3/4]
		for row in train_set[1:]:
			row[t] = float(row[t])
			if row[t] <= upper:
				row[t] = 'low'
			elif row[t] >= lower:
				row[t] = 'high'
			else:
				row[t] = 'med'

	if 'Longitude' in test_set[0]:
		t = test_set[0].index('Longitude')
		temp = list([row[t] for row in test_set[1:]])
		temp = map(float, temp)
		temp.sort()
		upper = temp[len(temp)/4]
		lower = temp[len(temp)*3/4]
		for row in test_set[1:]:
			row[t] = float(row[t])
			if row[t] <= upper:
				row[t] = 'low'
			elif row[t] >= lower:
				row[t] = 'high'
			else:
				row[t] = 'med'

	if 'Latitude' in test_set[0]:
		t = test_set[0].index('Latitude')
		temp = list([row[t] for row in test_set[1:]])
		temp = map(float, temp)
		temp.sort()
		upper = temp[len(temp)/4]
		lower = temp[len(temp)*3/4]
		for row in test_set[1:]:
			row[t] = float(row[t])
			if row[t] <= upper:
				row[t] = 'low'
			elif row[t] >= lower:
				row[t] = 'high'
			else:
				row[t] = 'med'
  	
  	root = CNode(train_set)
	BuildTree(root)

	Loss_square = 0
	for row in test_set[1:]:
		Loss_square += square_loss(test_set[0], row, root)
	Loss_square = float(Loss_square)/(len(test_set)-1)
	print 'SQUARED LOSS='+ "%.4f"%Loss_square


	print
	print
	print 'The data below is to test the models using 10-fold-cross-validation'
	print
	print

	#10-fold-cross-validation
	k = 10
	n = (len(train_set) - 1)/k
	indexList = []
	i = 0
	while i <= k:
		indexList.append(i*n + 1)
		i += 1
	
	copy = train_set[1:]
	random.shuffle(copy)
	train_set[1:] = copy

	trainning_set = list()
	testing_set = list()
	i = 0

	while i < 10:
		trainning_set.append(list())
		testing_set.append(list())
		trainning_set[i] = train_set[0:indexList[i]] + train_set[indexList[i+1]:indexList[k]]
		testing_set[i] = train_set[0:1] + train_set[indexList[i]:indexList[i+1]]
		i += 1


	example_num = [50, 100, 250, 500, 1000]
	square_loss_data = list()
	for i in example_num:
		Loss_square_mean = 0
		for j in range(0,10):
			temp_train_list = trainning_set[j][0:i+1]
			root = CNode(temp_train_list)
			BuildTree(root)
			Loss_square = 0
			#print testing_set[j][0]
			for row in testing_set[j][1:]:
				Loss_square += square_loss(testing_set[j][0], row, root)
			Loss_square = float(Loss_square)/(len(testing_set[j])-1)
			Loss_square_mean += Loss_square
		Loss_square_mean = float(Loss_square_mean)/10
		square_loss_data.append(Loss_square_mean)



	print square_loss_data


	




