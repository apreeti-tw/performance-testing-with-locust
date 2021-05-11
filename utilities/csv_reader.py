import csv


class CSVReader:
    def __init__(self, filepath):
        self.file_path = filepath

    def readCSV(self):
        reader = csv.DictReader(open(self.file_path))
        data = []
        for element in reader:
            data.append(element)
        return data
