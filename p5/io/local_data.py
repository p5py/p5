# for loading tables in csv format
from typing import List


class Table:
    """Class to represent tabular data

    :param path: Path to the CSV file.
    """

    def __init__(self, path: str, seperator: str):
        """
        Initializes Table object when given the path to a CSV file.
        """
        with open(path, "r") as file:
            lines = file.readlines()
        data = []
        for line in lines:
            fragment = line.split(seperator)
            x = fragment[-1]
            x = x[:-1]
            fragment[-1] = x
            data.append(fragment)
        self.data: List[List] = data

    def get_row_count(self) -> int:
        """
        :returns: Number of rows in the read CSV.
        """
        return len(self.data)

    def getRowCount(self) -> int:
        """
        :returns: Number of rows in the read CSV.
        """
        return self.get_row_count()

    def get_column_count(self) -> int:
        """
        :returns: Number of columns in the read CSV.
        """
        return len(self.data[0])

    def getColumnCount(self) -> int:
        """
        :returns: Number of columns in the read CSV.
        """
        return self.get_column_count()

    def get_column(self, name: str) -> List:
        """
        :param name: Name of the required column

        :returns: An entire column based on the column index.
        """
        count = self.data[0].index(name)
        return [item[count] for item in self.data]

    def getColumn(self, name: str) -> List:
        """
        :param name: Name of the required column

        :returns: An entire column based on the column index.
        """
        return self.get_column(name)

    def get_row(self, index: str) -> List:
        """
        Returns an entire row when given the row index.

        :param index: Name of the row

        :returns: An entire row when given the row index.
        """
        for fragment in self.data:
            if fragment[0] == index:
                return fragment

    def getRow(self, index: str) -> List:
        """
        Returns an entire row when given the row index.

        :param index: Name of the row

        :returns: An entire row when given the row index.
        """
        return self.get_row(index)

    def get_array(self):
        """
        :returns: the entire csv data as an multidimensional array.
        """
        return self.data

    def getArray(self):
        """
        :returns: the entire csv data as an multidimensional array.
        """
        return self.get_array()


def load_table(path: str, mode: str = "csv") -> Table:
    """
    Calls Table class and returns a Table class object

    :param path: Path to file

    :param mode: Type of File csv/ssv/tsv.

    :returns: A table object

    """
    assert mode in {"csv", "tsv"}
    if mode == "csv":
        seperator = ","
    elif mode == "ssv":
        seperator = ";"
    elif mode == "tsv":
        seperator = "\t"
    return Table(path, seperator)
