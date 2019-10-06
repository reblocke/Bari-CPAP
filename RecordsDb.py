# Contains classes to support Bari/SWC Database

import pandas as pd


class RecordsDb:
    """The class representing the entire database of patients included in the
    study, stored as a list
    Attributes:
        PatientArray: list of patient records
    """

    PatientArray = []

    def __init__(self):
        self.PatientArray = []

    def findPatient(self, mrn):
        """Find a patient record by MRN"""
        if len(self.PatientArray) == 0:
            return None
        for i in self.PatientArray:
            if i.MRN == mrn:
                return i
        return None

    def addPatient(self, patient):
        """add a patient record to the PatientArray"""
        self.PatientArray.append(patient)

    def size(self):
        """returns size of the Patient Array (= all records)"""
        return len(self.PatientArray)

    def AHIList(self):
        """returns a list of the AHIs in the db"""
        AHIs = []
        for record in self.PatientArray:
            AHIs.append(record.Diag_AHI)
        return AHIs

    def WeightDOSList(self):
        """returns a list of the patients' weight at the time of surgery"""
        Weights = []
        for record in self.PatientArray:
            if len(record.Weights) > 0:
                Weights.append(record.Weights[0])
            else:
                Weights.append(None)
        return pd.Series(Weights)

    def WeightLossList(self):
        """returns a list of the patient's lightest weight"""
        Weights = []
        for record in self.PatientArray:
            Weights.append(record.maxWeightLoss())
        return pd.Series(Weights)

    def WeightRegainList(self):
        """returns a list of the patient's weight regain, defined as lightest
        weight subtracted from last weight"""
        Weights = []
        for record in self.PatientArray:
            Weights.append(record.weightRegain())
        return pd.Series(Weights)

    def createDataFrame(self):
        """Exports the data contained in db as a Pandas data frame in the
        following format:
        MRN = index
        Factors:
        weight regain (primary outcome)
        maximum weight loss
        BMI DOS
        Diag AHI
        Avg CPAP Compliance
        """

        index = list()
        weight_regain = list()
        max_wt_loss = list()
        BMI_DOS = list()
        pt_diag_AHI = list()
        pt_avg_comp = list()
        for patient in self.PatientArray:
            index.append(patient.MRN)
            weight_regain.append(patient.weightRegain())
            max_wt_loss.append(patient.maxWeightLoss())
            BMI_DOS.append(patient.BMIDOS())
            pt_diag_AHI.append(patient.Diag_AHI)
            pt_avg_comp.append(patient.avgCompliance())

        return pd.DataFrame({'mrn': index, 'wrg':weight_regain, 'mwl':max_wt_loss, 'bmi':BMI_DOS, 'dAHI':pt_diag_AHI, 'pac':pt_avg_comp})

    def printDb(self):
        for record in self.PatientArray:
            record.printPtRecord()
            print("----")


class PatientRecord:
    """Class representing each individual, as indexed by MRN, in the study.
    Attributes:
    Diag_AHI: diagnostic AHI
    Diag_AHI_Date: the date of that study
    Compliance_Records: any compliance downloads that have occured
    Bari_Surg_date: their bariatric surgery date
    Height_DOS: their height in cm at surgery
    Weights: their weight in kg at surgery and 8 additional time points,
    stored as a list [DOS, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y].
    """

    MRN = None
    Diag_AHI = None
    Diag_AHI_Date = None
    Compliance_Records = None
    Bari_Surg_Date = None
    Height_DOS = None
    Weights = None  # [DOS, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y]. Kgs

    def __init__(self, mrn):
        self.MRN = mrn
        self.Diag_AHI = None
        self.Diag_AHI_Date = None
        self.Compliance_Records = list()
        self.Bari_Surg_Date = None
        self.Height_DOS = None
        self.Weights = list()

    def setAHI(self, diag_ahi, diag_ahi_date):
        self.Diag_AHI = diag_ahi
        self.Diag_AHI_Date = diag_ahi_date

    def setBariDOS(self, surg_date):
        self.Bari_Surg_Date = surg_date

    def setHeight(self, height):
        self.Height_DOS = height

    def setWeights(self, weights):
        """takes an array of weights"""
        self.Weights = weights

    def weightDOS(self):
        try:
            return self.Weights[0]
        except (TypeError, ValueError):
            return None

    def addComplianceRecord(self, record):
        self.Compliance_Records.append(record)

    def numComplianceRecords(self):
        return len(self.Compliance_Records)

    def numDaysComplianceRecords(self):
        """Returns the total number of days included in compliance records"""
        days = 0
        for i in self.Compliance_Records:
            days = days + i.days
        return days

    def avgCompliance(self):
        days = 0
        abs_days_used_4h = 0
        if self.numComplianceRecords() == 0:
            return 0
        for i in self.Compliance_Records:
            days = days + i.days
            abs_days_used_4h = abs_days_used_4h + (i.days * i.days_used_4h)
        if days == 0:
            return 0.0
        else:
            return abs_days_used_4h / days

    def BMIDOS(self):
        return self.BMI_at_time(0)

    def BMI_at_time(self, index):
        """ weight (kg) / height(m)^2.
        [DOS, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y]. Kgs"""
        if len(self.Weights) > 0 and self.Weights[index] is not None:
            if self.Height_DOS is not None:
                return self.Weights[index] / ((float(self.Height_DOS) / 100) ** 2)
        return None

    def maxWeightLoss(self):
        """returns weight at surgery minus lightest weight. None if there is
        no weight recorded at surgery"""
        if len(self.Weights) is 0 or self.Weights[0] is None:
            return None
        else:
            min = self.Weights[0]
            for weight in self.Weights:
                if weight is not None and weight < min:
                    min = weight
            return self.Weights[0] - min

    def weightRegain(self):
        """returns last weight minus lightest weight"""
        min = 9999  # larger than largest
        for weight in self.Weights:
            if weight is not None and weight < min:
                min = weight
        last = None
        for i in range(0, len(self.Weights)):
            if self.Weights[i] is not None:
                last = self.Weights[i]
        if last is None:
            return None
        else:
            return last - min

    def printPtRecord(self):
        print("MRN: " + str(self.MRN) + ", Diag_AHI: " + str(self.Diag_AHI))
        print("DOS:" + str(self.Bari_Surg_Date) + " @ BMI: " + str(self.BMIDOS()))
        print("Weights: " + str(self.Weights))
        print("Diagnostic AHI: " + str(self.Diag_AHI) + " on " + str(self.Diag_AHI_Date))
        print("Total of " +str(len(self.Compliance_Records)) + " compliance records")
        for i in self.Compliance_Records:
            i.printCompRecord()
        print("Avg 4h+ compliance: " + str(self.avgCompliance()))
        print("Based on " + str(self.numDaysComplianceRecords()) + " days of records")


class complianceReport:
    """Represents one compliance report downloaded from a CPAP remote
    vender such as resmed or respironics. Includes the date of download, the
    number of days that the download was of, and the percentage of days
    with over 4h of use"""

    date = None
    days = 0
    days_used_4h = 0

    def __init__(self, date, days, days_used_4h):
        self.date = date
        if days is None:
            self.days = 0
        else:
            self.days = int(days)
        if days_used_4h is None:
            self.days_used_4h = 0.0
        else:
            self.days_used_4h = float(days_used_4h)  # percentage

    def printCompRecord(self):
        print(str(self.date) +": Used 4+ h on " + str(self.days_used_4h) + "% of last " +str (self.days) + " days")
