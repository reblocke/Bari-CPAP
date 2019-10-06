# This script is for accessing the Bariatric CPAP Db excel spreadsheet
from openpyxl import load_workbook
import pandas as pd
from RecordsDb import *

# Locations
db_loc = "/Users/reblocke/Box/Residency Personal Files/Scholarly Work/Bariatric CPAP Project/Bariatric Clinic data/"
compliance_db_loc = "BARI_SLEEP_CPAP_COMPLIANCE_092619.xlsx"
outcome_db_loc = "BARI_SLEEP_031919 from EDW - edits.xlsx"
compliance_data_sheet_name = "Sheet 1"
outcome_data_sheet_name = "Sheet 1"

def load_sheet(location, sheet_name):
    """loads the sheet excel doc and returns the compliance sheet"""
    db = load_workbook(location, read_only=True, data_only=True)
    return db[sheet_name]


def create_patient_db(compliance_sheet, outcomes_sheet):
    """Excel spreadsheet columns of interest"""
    Patients = RecordsDb()
    Patients = process_Outcomes_Db(Patients, outcomes_sheet)
    Patients = process_Adherence_db(Patients, compliance_sheet)
    return Patients


def process_Adherence_db(Patients, compliance_sheet):
    """takes patient db and fills it with info based on compliance sheet"""
    MRN_Column = "A"
    Diag_AHI_Column = "Q"
    Diag_AHI_Date_Column = "S"
    Percent_Days_4_Hours_Column = "F"
    Num_Days_Reported_Column = "G"
    Download_Date_Column = "B"
    i = 2  # The row the data starts on

    print("Processing Adherence")

    while compliance_sheet["A"+str(i)].value is not None:
        # For each row that has an MRN entry...
        row_mrn = int(compliance_sheet[MRN_Column + str(i)].value)
        try:
            row_ahi = float(compliance_sheet[Diag_AHI_Column+str(i)].value)
        except (ValueError, TypeError):
            row_ahi = None
        row_ahi_date = compliance_sheet[Diag_AHI_Date_Column+str(i)].value

        try:
            percent_days_4_hours = float(compliance_sheet[Percent_Days_4_Hours_Column+str(i)].value)
        except (ValueError, TypeError):
            percent_days_4_hours = None

        try:
            num_days_reported = int(compliance_sheet[Num_Days_Reported_Column+str(i)].value)
        except (ValueError, TypeError):
            num_days_reported = None

        download_date = compliance_sheet[Download_Date_Column+str(i)].value

        row_compliance = complianceReport(download_date, num_days_reported, percent_days_4_hours)

        print("Processing adherence record number " + str(i-1))
        Patient = Patients.findPatient(row_mrn)
        if Patient is None:
            # Patient is not already in list
            Patient = PatientRecord(row_mrn)
            Patients.addPatient(Patient)
        Patient.setAHI(row_ahi, row_ahi_date)
        Patient.addComplianceRecord(row_compliance)
        i = i+1
    return Patients


def process_Outcomes_Db(Patients, outcomes_sheet):
    """takes patient db and fills it based on outcomes excel spreadsheet"""
    MRN_Column = "A"
    Bari_Surg_Date_Column = "B"
    Height_DOS_Column = "C"
    Weight_DOS_Column = "L"
    Weight_2mo_Column = "M"
    Weight_4mo_Column = "N"
    Weight_6mo_Column = "O"
    Weight_1y_Column = "P"
    Weight_2y_Column = "Q"
    Weight_3y_Column = "R"
    Weight_4y_Column = "S"
    Weight_5y_Column = "T"

    weightOrder = [Weight_DOS_Column, Weight_2mo_Column, Weight_4mo_Column, Weight_6mo_Column, Weight_1y_Column, Weight_2y_Column, Weight_3y_Column, Weight_4y_Column, Weight_5y_Column]

    print("Processing Outcomes")
    i = 2  # The row the data starts on

    while outcomes_sheet["A"+str(i)].value is not None:
        # For each row that has an MRN entry...
        print("Processing outcome chart #" + str(i-1))
        row_mrn = outcomes_sheet[MRN_Column + str(i)].value
        row_bari_dos = outcomes_sheet[Bari_Surg_Date_Column+str(i)].value
        try:
            row_height_dos = float(outcomes_sheet[Height_DOS_Column+str(i)].value)
        except(ValueError, TypeError):
            row_height_dos = None

        row_weight = list() #order of appending is chronological
        for column in weightOrder:
            try:
                row_weight.append(float(outcomes_sheet[column+str(i)].value))
            except(ValueError, TypeError):
                row_weight.append(None)

        Patient = Patients.findPatient(row_mrn)
        if Patient is None:
            # Patient is not already in list
            Patient = PatientRecord(row_mrn)
            Patients.addPatient(Patient)
        if row_height_dos is not None:
            Patient.setHeight(row_height_dos)
        if len(row_weight) is not 0:
            Patient.setWeights(row_weight)
        if row_bari_dos is not None:
            Patient.setBariDOS(row_bari_dos)
        i = i+1
    return Patients


def test_db_gen():
    db = RecordsDb()
    patient1 = PatientRecord("1243")
    patient1.setAHI("41", "12/19/19")
    record1 = complianceReport("12/21/19", 90, 50)
    record2 = complianceReport("12/21/18", 30, 100)
    patient1.addComplianceRecord(record1)
    patient1.addComplianceRecord(record2)
    patient1.setHeight(185)
    patient1.setWeights([150, 140, 140, 140, 130, 140, 145, None, 160])
    # [DOS, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y]
    print(patient1.BMIDOS())
    db.addPatient(patient1)

    patient2 = PatientRecord("1244")
    patient2.setAHI("40", "12/19/20")
    record3 = complianceReport("12/21/19", 90, 45)
    record4 = complianceReport("12/21/18", 30, 0)
    patient2.addComplianceRecord(record3)
    patient2.addComplianceRecord(record4)
    patient2.setHeight(150)
    patient2.setWeights([130, 135, 140, 140, 130, 140, 145, 155, None])
    db.addPatient(patient2)

    patient3 = PatientRecord("1245")
    patient3.setAHI(None, None)
    patient3.setHeight(190)
    patient3.setWeights([100, None, None, None, None, None, None, None, None])
    db.addPatient(patient3)

    print("----")
    patient1.printPtRecord()
    patient2.printPtRecord()
    print("----")
    return db


def main():
    # 1 for testing, 0 to run
    testing_mode = 1

    if testing_mode == 0:
        database = test_db_gen()
    else:
        outcomes_sheet = load_sheet(db_loc + outcome_db_loc, outcome_data_sheet_name)
        compliance_sheet = load_sheet(db_loc + compliance_db_loc, compliance_data_sheet_name)
        database = create_patient_db(compliance_sheet, outcomes_sheet)

    database.printDb()

    # Summary Statistics:

    AHIList = database.AHIList()
    i = []
    for AHI in AHIList:
        if AHI is not None:
            i.append(AHI)
    print("Number of AHIs: " + str(len(i)))
    ObtainedAHIs = pd.Series(i)
    print("Median: " + str(ObtainedAHIs.median()))
    print("Std Dev: " + str(ObtainedAHIs.std()))

    print("\nWeight On Day of Surgery (Kg):")
    print(database.WeightDOSList().describe())

    print("\nWeight Loss Acheived (Kg):")
    print(database.WeightLossList().describe())

    print("\nWeight Regain Observed (Kg):")
    print(database.WeightRegainList().describe())

    df = database.dataFrameExport()


if __name__ == '__main__':
    main()
