#for loading tables in csv format
class Table:
	"""Class to represent tabular data

	:param path: Path to the CSV file.
	:type path: string
	"""

	def __init__(self,path,seperator):
		"""
		Initializes Table object when given the path to a CSV file.
		"""
		file = open(path,'r')
		lines = file.readlines()
		data = []
		for line in lines:
			fragment = line.split(seperator)
			x = fragment[len(fragment)-1]
			x = x[:-1]
			fragment[len(fragment)-1] = x
			data.append(fragment)
		self.data = data

	def get_row_count(self):
		"""
		:returns: Number of rows in the read CSV.
		:rtype: int
		"""
		return len(self.data)

	def get_column_count(self):
		"""
		:returns: Number of columns in the read CSV.
		:rtype: int
		"""
		return len(self.data[0])

	def get_column(self,name):
		"""
		:param name: Name of the required column
		:type name: string

		:returns: An entire column based on the column name.
		:rtype: list 
		"""
		count = 0
		for i in self.data[0]:
			if i == name:
				break
			count = count + 1
		column = []
		for item in self.data:
			column.append(item[count])
		return column

	def get_row(self,index):
		"""
		:param index: Index of the required row.
		:type index: int

		:returns: An entire row when given the row index.
		:rtype: list
		"""
		return self.data[index]
	def get_array(self):
		"""
		:returns: the entire csv data as an multidimensional array.
		:rtype: list
		"""
		return self.data


def load_table(path,mode):
	"""
	Calls the Table class.
	
	:param path: Path to file
	:type path: string

	:param mode: Type of File csv/ssv.
	:type mode: string

	:returns: A Table object
	:rtype: object
	"""
	if mode == "csv":
		seperator = ','
	if mode == "ssv":
		seperator = ';'

	table = Table(path,seperator)
	return table  
