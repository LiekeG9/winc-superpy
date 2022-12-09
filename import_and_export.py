import constants
import csv
import classes
import helpers

# generic export method for all data which must be stored as CSV files
def export_to_csv(fFilename, fFields, fObjList):
    with open(fFilename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=";")
        csvwriter.writerow(fFields)
        for obj in fObjList:
            row = []
            for key, value in obj.__dict__.items():
                row.append(str(value))
            csvwriter.writerow(row)

# generic import method for both Bought.csv and Sold.csv files
def import_from_csv(fFilename, fFields, fObjList):
    helpers.CreateFileIfNotExists(fFilename, fFields)
    fObjList.clear()
    with open(fFilename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        fields = next(csvreader)
        for row in csvreader:
            if len(row) == 5: # when buying, use 5 columns to create new instance
                fObjList.append(classes.Bought(row[0], row[1], row[2], row[3], row[4], fObjList))
            if len(row) == 4: # when selling, use 4 columns to create new instance
                fObjList.append(classes.Sold(row[0], row[1], row[2], row[3], fObjList))
