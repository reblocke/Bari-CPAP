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
    MRN_Column = 0  # "A"
    Diag_AHI_Column = 16  # "Q"
    Diag_AHI_Date_Column = 18 # "S"
    Percent_Days_4_Hours_Column = 5  # "F"
    Num_Days_Reported_Column = 6  # "G"
    Download_Date_Column = 1  # "B"
    i = 1

    print("Processing Adherence")

    compliance_iter = compliance_sheet.iter_rows()
    next(compliance_iter)  # skip first row
    for patient_row in compliance_iter:
        try:
            row_mrn = int(patient_row[MRN_Column].value)
        except (ValueError, TypeError):
            row_mrn = None
        try:
            row_ahi = float(patient_row[Diag_AHI_Column].value)
        except (ValueError, TypeError):
            row_ahi = None
        try:
            row_ahi_date = patient_row[Diag_AHI_Date_Column].value
        except (ValueError, TypeError):
            row_ahi_date = None
        try:
            percent_days_4_hours = float(patient_row[Percent_Days_4_Hours_Column].value)
        except (ValueError, TypeError):
            percent_days_4_hours = None
        try:
            num_days_reported = int(patient_row[Num_Days_Reported_Column].value)
        except (ValueError, TypeError):
            num_days_reported = None
        try:
            download_date = patient_row[Download_Date_Column].value
        except (ValueError, TypeError):
            download_date = None

        row_compliance = complianceReport(download_date, num_days_reported,
            percent_days_4_hours)

        # print("Processing adherence record number " + str(i-1))
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
    MRN_Column = 0  # "A"
    Bari_Surg_Date_Column = 1  # "B"
    Height_DOS_Column = 2   # "C"
    Weight_DOS_Column = 11  # "L"
    Weight_2mo_Column = 12  # "M"
    Weight_4mo_Column = 13  # "N"
    Weight_6mo_Column = 14  # "O"
    Weight_1y_Column = 15  # "P"
    Weight_2y_Column = 16  # "Q"
    Weight_3y_Column = 17  # "R"
    Weight_4y_Column = 18  # "S"
    Weight_5y_Column = 19  # "T"

    weightOrder = [Weight_DOS_Column, Weight_2mo_Column, Weight_4mo_Column,
        Weight_6mo_Column, Weight_1y_Column, Weight_2y_Column, Weight_3y_Column,
        Weight_4y_Column, Weight_5y_Column]

    print("Processing Outcomes")
    i = 1  # The row the data starts on

    outcomes_iter = outcomes_sheet.iter_rows()
    next(outcomes_iter)  # skip 1st/labels
    for patient_row in outcomes_iter:
        # For each row that has an MRN entry...
        # print("Processing chart #" + str(i))
        try:
            row_mrn = int(patient_row[MRN_Column].value)
        except(ValueError, TypeError):
            row_mrn = None
        row_bari_dos = patient_row[Bari_Surg_Date_Column].value

        try:
            row_height_dos = float(patient_row[Height_DOS_Column].value)
        except(ValueError, TypeError):
            row_height_dos = None

        row_weight = list()  # order of appending is chronological
        for column in weightOrder:
            try:
                row_weight.append(float(patient_row[column].value))
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
    patient1 = PatientRecord(1243)
    patient1.setAHI(41.0, "12/19/19")
    record1 = complianceReport("12/21/19", 90, 50)
    record2 = complianceReport("12/21/18", 30, 100)
    patient1.addComplianceRecord(record1)
    patient1.addComplianceRecord(record2)
    patient1.setHeight(185.0)
    patient1.setWeights(
        [150.0, 140.0, 140.0, 140.0, 130.0, 140.0, 145.0, None, 160.0])
    # [DOS, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y]
    print(patient1.BMIDOS())
    db.addPatient(patient1)

    patient2 = PatientRecord(1244)
    patient2.setAHI(40.0, "12/19/20")
    record3 = complianceReport("12/21/19", 90, 45)
    record4 = complianceReport("12/21/18", 30, 0)
    patient2.addComplianceRecord(record3)
    patient2.addComplianceRecord(record4)
    patient2.setHeight(150.0)
    patient2.setWeights(
        [130.0, 135.0, 140.0, 140.0, 130.0, 140.0, 145.0, 155.0, None])
    db.addPatient(patient2)

    patient3 = PatientRecord(1245)
    patient3.setAHI(None, None)
    patient3.setHeight(190.0)
    patient3.setWeights([100.0, None, None, None, None, None, None, None, None])
    db.addPatient(patient3)

    print("----")
    patient1.printPtRecord()
    patient2.printPtRecord()
    print("----")
    return db


def main():
    # 0 for testing, 1 to run
    testing_mode = 1

    if testing_mode == 0:
        database = test_db_gen()
    else:
        # This could have been done more elegantly w/ dataframe merge + groupby?
        compliance_sheet = load_sheet(db_loc + compliance_db_loc, compliance_data_sheet_name)
        outcomes_sheet = load_sheet(db_loc + outcome_db_loc, outcome_data_sheet_name)
        database = create_patient_db(compliance_sheet, outcomes_sheet)


    print("\nWeight On Day of Surgery (Kg):")
    print(database.WeightDOSList().describe())

    print("\nWeight Loss Acheived (Kg):")
    print(database.WeightLossList().describe())

    print("\nWeight Regain Observed (Kg):")
    print(database.WeightRegainList().describe())

    df = database.createDataFrame()

    # Print Stats for the subset with compliance data and without
    print("\nThose w/ compliance data")
    print(df[df['Avg Compliance'] > 0.0].describe())
    print("\nthose w/o compliance data")
    print(df[df['Avg Compliance'] == 0.0].describe())

    # Print Stats for the subset with a diagnostic AHI
    print("\nThose w/ diagnostic AHI")
    print(df[df['Diag AHI'].notnull()].describe())



    df.to_excel('output.xlsx')


if __name__ == '__main__':
    main()
