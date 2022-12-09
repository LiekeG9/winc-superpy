import helpers
import constants
import datetime

report_date = "1900-01-01"

# load current date from file
def LoadReportDateFromFile():
    global report_date
    helpers.CreateFileIfNotExists(constants.FILE_CURRENT_DATE, [datetime.datetime.today().strftime("%Y-%m-%d")])
    with open(constants.FILE_CURRENT_DATE) as f:
        tmpLines = f.readlines()
    report_date = tmpLines[0].strip()

# save current date to file
def SaveReportDateToFile(fAdvanceTime):
    tmpToday = datetime.datetime.now()
    tmpNewDate = tmpToday + datetime.timedelta(days=fAdvanceTime)
    with open(constants.FILE_CURRENT_DATE, 'w') as f:
        f.write(tmpNewDate.strftime("%Y-%m-%d"))
