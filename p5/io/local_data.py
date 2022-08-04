# for loading tables in csv format
class Table:
    """Class to represent tabular data

    :param path: Path to the CSV file.
    :type path: string
    """

    def __init__(self, path, seperator):
        """
        Initializes Table object when given the path to a CSV file.
        """
        file = open(path, "r")
        lines = file.readlines()
        data = []
        for line in lines:
            fragment = line.split(seperator)
            x = fragment[len(fragment) - 1]
            x = x[:-1]
            fragment[len(fragment) - 1] = x
            data.append(fragment)
        self.data = data

    def get_row_count(self):
        """
        :returns: Number of rows in the read CSV.
        :rtype: int
        """
        return len(self.data)

    def getRowCount(self):
        """
        :returns: Number of rows in the read CSV.
        :rtype: int
        """
        return self.get_row_count()

    def get_column_count(self):
        """
        :returns: Number of columns in the read CSV.
        :rtype: int
        """
        return len(self.data[0])

    def getColumnCount(self):
        """
        :returns: Number of columns in the read CSV.
        :rtype: int
        """
        return self.get_column_count()

    def get_column(self, name):
        """
        :param name: Name of the required column
        :type name: string

        :returns: An entire column based on the column index.
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

    def getColumn(self, name):
        """
        :param name: Name of the required column
        :type name: string

        :returns: An entire column based on the column index.
        :rtype: list
        """
        return self.get_column(name)

    def get_row(self, index):
        """
        Returns an entire row when given the row index.

        :param index: Name of the row
        :type index: string

        :returns: An entire row when given the row index.
        :rtype: list
        """
        for fragment in self.data:
            if fragment[0] == index:
                return fragment

    def getRow(self, index):
        """
        Returns an entire row when given the row index.

        :param index: Name of the row
        :type index: string

        :returns: An entire row when given the row index.
        :rtype: list
        """
        return self.get_row(index)

    def get_array(self):
        """
        :returns: the entire csv data as an multidimensional array.
        :rtype: list
        """
        return self.data

    def getArray(self):
        """
        :returns: the entire csv data as an multidimensional array.
        :rtype: list
        """
        return self.get_array()


def load_table(path, mode="csv"):
    """
    Calls Table class and returns a Table class object

    :param path: Path to file
    :type path: string

    :param mode: Type of File csv/ssv/tsv.
    :type mode: string

    :returns: A table object
    :rtype: object

    """
    if mode == "csv":
        seperator = ","
    if mode == "ssv":
        seperator = ";"
    if mode == "tsv":
        seperator = "\t"
    table = Table(path, seperator)
    return table
