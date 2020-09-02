#for loading tables in csv format
class Table:

	def __init__(self,path):
		"""
		Initializes Table object when given the path to a CSV file.

		:param PATH: Path to the CSV file.
		:type PATH: string
		"""
		file = open(path,'r')
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
		"""
		Returns number of rows in the read CSV.
		"""
		return len(self.data)

	def get_column_count(self):
		"""
		Returns number of columns in the read CSV.
		"""
		return len(self.data[0])

	def get_column(self,name):
		"""
		Returns an entire column based on the column index.

		:param name: Name of the required column
		:type name: string
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
		Returns an entire row when given the row index.

		:param index: Name of the row
		:type index: string
		"""
		for fragment in self.data:
			if fragment[0] == index:
				return fragment
	def get_array(self):
		"""
		Returns the entire csv data as an multidimensional array.
		"""
		return self.data


def load_table(path):
	"""
	Calls Table class and returns a Table class object
	
	:param PATH: Path to file
	:type PATH: string
	"""
	table = Table(path)
	return table  
