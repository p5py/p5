#for loading tables in csv format
class Table:

	def __init__(self,PATH):
		file = open(PATH,'r')
		lines = file.readlines()
		data = []
		for line in lines:
			fragment = line.split(',')
			x = fragment[len(fragment)-1]
			x = x[:-1]
			fragment[len(fragment)-1] = x
			data.append(fragment)
		self.data = data

	def get_row_count(self):
		return (len(self.data))

	def get_column_count(self):
		return (len(self.data[0]))

	def get_column(self,name):
		count = 0
		for i in self.data[0]:
			if i == name:
				break
			count = count + 1
		column = []
		for item in self.data:
			column.append(item[count])
		return column

	def get_row(self,inde):
		for fragment in self.data:
			if fragment[0] == inde:
				return fragment
	def get_array(self):
		return self.data
