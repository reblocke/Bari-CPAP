# Contains classes to support Bari/SWC Database

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime

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
        """Exports the data contained in db as a Pandas data frame
        """

        index = list()
        dob = list()
        dos = list()
        study_date = list()
        age_at_dos = list()
        study_to_dos = list()
        pre_op_date = list()
        sex = list()
        cci = list()
        weight_DOS = list()
        ibw = list()
        pre_op_creat = list()
        min_weight = list()
        min_weight_time = list()
        last_weight = list()
        last_weight_time = list()
        weight_regain = list()
        max_wt_loss = list()
        BMI_DOS = list()
        pt_diag_AHI = list()
        pt_avg_comp = list()
        pt_comp_days = list()
        pt_max_wt_loss_pct = list()
        two_mo_weight = list()
        four_mo_weight = list()
        six_mo_weight = list()
        one_y_weight = list()
        two_y_weight = list()
        three_y_weight = list()
        four_y_weight = list()
        five_y_weight = list()
        two_mo_EWL = list()
        four_mo_EWL = list()
        six_mo_EWL = list()
        one_y_EWL = list()
        two_y_EWL = list()
        three_y_EWL = list()
        four_y_EWL = list()
        five_y_EWL = list()
        pre_op_HCO3 = list()
        two_mo_HCO3 = list()
        four_mo_HCO3 = list()
        six_mo_HCO3 = list()
        one_y_HCO3 = list()
        two_y_HCO3 = list()
        three_y_HCO3 = list()
        four_y_HCO3 = list()
        five_y_HCO3 = list()
        two_mo_delta_HCO3 = list()
        four_mo_delta_HCO3 = list()
        six_mo_delta_HCO3 = list()
        one_y_delta_HCO3 = list()
        two_y_delta_HCO3 = list()
        three_y_delta_HCO3 = list()
        four_y_delta_HCO3 = list()
        five_y_delta_HCO3 = list()
        min_HCO3 = list()
        min_HCO3_time = list()
        all_post_op_HCO3s_below_25 = list()
        mean_post_op_HCO3 = list()
        # [DOS/Preop, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y].
        loop_exclusion = list()
        opiate_exclusion = list()
        ca_exclusion = list()
        other_exclusion = list()


        i = 1
        for patient in self.PatientArray:
            index.append(i)  # (patient.MRN) if using real MRN
            i = i+1
            sex.append(patient.getSex())
            dob.append(patient.getDOB())
            dos.append(patient.getDOS())
            study_date.append(patient.getStudyDate())
            age_at_dos.append(patient.getAgeAtDOS())
            study_to_dos.append(patient.getStudyDOSTime())
            pre_op_date.append(patient.getPreOpDate())
            cci.append(patient.getCCI())
            ibw.append(patient.getIBW())
            pre_op_creat.append(patient.getPreOpCreat())
            weight_regain.append(patient.weightRegain())
            weight_DOS.append(patient.weightDOS())
            min_weight.append(patient.getMinWeight())
            min_weight_time.append(patient.minWeightTime())
            last_weight.append(patient.getLastWeight())
            last_weight_time.append(patient.lastWeightTime())
            max_wt_loss.append(patient.maxWeightLoss())
            BMI_DOS.append(patient.BMIDOS())
            pt_diag_AHI.append(patient.Diag_AHI)
            pt_avg_comp.append(patient.avgCompliance())
            pt_comp_days.append(patient.numDaysComplianceRecords())
            pt_max_wt_loss_pct.append(patient.percentWeightLoss())
            two_mo_weight.append(patient.getWeights()[1])
            four_mo_weight.append(patient.getWeights()[2])
            six_mo_weight.append(patient.getWeights()[3])
            one_y_weight.append(patient.getWeights()[4])
            two_y_weight.append(patient.getWeights()[5])
            three_y_weight.append(patient.getWeights()[6])
            four_y_weight.append(patient.getWeights()[7])
            five_y_weight.append(patient.getWeights()[8])
            two_mo_EWL.append(patient.getEWL()[1])
            four_mo_EWL.append(patient.getEWL()[2])
            six_mo_EWL.append(patient.getEWL()[3])
            one_y_EWL.append(patient.getEWL()[4])
            two_y_EWL.append(patient.getEWL()[5])
            three_y_EWL.append(patient.getEWL()[6])
            four_y_EWL.append(patient.getEWL()[7])
            five_y_EWL.append(patient.getEWL()[8])
            pre_op_HCO3.append(patient.getHCO3s()[0]) # pre-op
            two_mo_HCO3.append(patient.getHCO3s()[1])
            four_mo_HCO3.append(patient.getHCO3s()[2])
            six_mo_HCO3.append(patient.getHCO3s()[3])
            one_y_HCO3.append(patient.getHCO3s()[4])
            two_y_HCO3.append(patient.getHCO3s()[5])
            three_y_HCO3.append(patient.getHCO3s()[6])
            four_y_HCO3.append(patient.getHCO3s()[7])
            five_y_HCO3.append(patient.getHCO3s()[8])
            two_mo_delta_HCO3.append(patient.getDeltaHCO3s()[1])
            four_mo_delta_HCO3.append(patient.getDeltaHCO3s()[2])
            six_mo_delta_HCO3.append(patient.getDeltaHCO3s()[3])
            one_y_delta_HCO3.append(patient.getDeltaHCO3s()[4])
            two_y_delta_HCO3.append(patient.getDeltaHCO3s()[5])
            three_y_delta_HCO3.append(patient.getDeltaHCO3s()[6])
            four_y_delta_HCO3.append(patient.getDeltaHCO3s()[7])
            five_y_delta_HCO3.append(patient.getDeltaHCO3s()[8])
            loop_exclusion.append(patient.get_loop_exclusion())
            opiate_exclusion.append(patient.get_opiate_exclusion())
            ca_exclusion.append(patient.get_ca_exclusion())
            other_exclusion.append(patient.get_other_exclusion())
            min_HCO3.append(patient.getMinHCO3()[1])
            min_HCO3_time.append(patient.getMinHCO3()[0])
            all_post_op_HCO3s_below_25.append(patient.all_hco3_below_25())
            mean_post_op_HCO3.append(patient.getMeanPostOpHCO3())

        return pd.DataFrame({'MRN': index,
                                'Sex': sex,
                                'DOB': dob,
                                'DOS': dos,
                                "Study Date": study_date,
                                'Age at Surgery': age_at_dos,
                                'Study Surgery Time': study_to_dos,
                                'Pre Op Date': pre_op_date,
                                'CCI': cci,
                                'IBW': ibw,
                                'Pre Op sCr': pre_op_creat,
                                'DOS Weight': weight_DOS,
                                '2mo Weight': two_mo_weight,
                                '4mo Weight': four_mo_weight,
                                '6mo Weight': six_mo_weight,
                                '1y Weight': one_y_weight,
                                '2y Weight': two_y_weight,
                                '3y Weight': three_y_weight,
                                '4y Weight': four_y_weight,
                                '5y Weight': five_y_weight,
                                '2mo EWL': two_mo_EWL,
                                '4mo EWL': four_mo_EWL,
                                '6mo EWL': six_mo_EWL,
                                '1y EWL': one_y_EWL,
                                '2y EWL': two_y_EWL,
                                '3y EWL': three_y_EWL,
                                '4y EWL': four_y_EWL,
                                '5y EWL': five_y_EWL,
                                'Min Weight': min_weight,
                                'Min Weight Time': min_weight_time,
                                'Last Weight': last_weight,
                                'Last Weight Time': last_weight_time,
                                'Weight Regain': weight_regain,
                                'Max Weight Loss': max_wt_loss,
                                'BMI': BMI_DOS,
                                'Pre Op HCO3': pre_op_HCO3,
                                '2mo HCO3': two_mo_HCO3,
                                '4mo HCO3': four_mo_HCO3,
                                '6mo HCO3': six_mo_HCO3,
                                '1y HCO3': one_y_HCO3,
                                '2y HCO3': two_y_HCO3,
                                '3y HCO3': three_y_HCO3,
                                '4y HCO3': four_y_HCO3,
                                '5y HCO3': five_y_HCO3,
                                '2mo Delta HCO3': two_mo_delta_HCO3,
                                '4mo Delta HCO3': four_mo_delta_HCO3,
                                '6mo Delta HCO3': six_mo_delta_HCO3,
                                '1y Delta HCO3': one_y_delta_HCO3,
                                '2y Delta HCO3': two_y_delta_HCO3,
                                '3y Delta HCO3': three_y_delta_HCO3,
                                '4y Delta HCO3': four_y_delta_HCO3,
                                '5y Delta HCO3': five_y_delta_HCO3,
                                'Min HCO3': min_HCO3,
                                'Min HCO3 Time': min_HCO3_time,
                                'All HCO3 Below 25': all_post_op_HCO3s_below_25,
                                'Mean HCO3 Post Op': mean_post_op_HCO3,
                                'Diag AHI': pt_diag_AHI,
                                'Avg Compliance': pt_avg_comp,
                                'Days Comp Records': pt_comp_days,
                                'Max Weight Loss Pct': pt_max_wt_loss_pct,
                                'Loop Exclusion': loop_exclusion,
                                'Opiate Exclusion': opiate_exclusion,
                                'CA Exclusion': ca_exclusion,
                                'Other Exclusion': other_exclusion})

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
    HCO3s = None  # [DOS, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y]. mEq/L
    Pre_Op_Date = None
    Pre_Op_sCr = None

    # Sex = None  Revisit once gender added to Db

    def __init__(self, mrn):
        if mrn is None:
            self.MRN = 0
        else:
            self.MRN = mrn
        self.Diag_AHI = None
        self.Diag_AHI_Date = None
        self.Compliance_Records = list()
        self.Bari_Surg_Date = None
        self.Height_DOS = None
        self.Weights = list()
        self.HCO3s = list()
        self.percExWtLossByTime = list()  # Add
        self.HCO3ChangeSinceSurg = list()  # Add
        self.IBW = None
        self.Index = None
        self.Sex = None
        self.DOB = None
        self.Age = None
        self.CCI = None
        self.Pre_Op_Date = None
        self.Pre_Op_sCr = None
        self.exclusions = None  # [ loop, opiate, ca inhib, other ]

    def setSex(self, sex_str):
        self.Sex = sex_str

    def setDOB(self, dob_date_obj):
        # Also sets AGE if Bari_Surg_Date has been set
        self.DOB = dob_date_obj
        if self.Bari_Surg_Date is None:
            return
        else:
            self.Age = relativedelta(self.Bari_Surg_Date, dob_date_obj).years

    def set_exclusions(self, loop_exclusion, opiate_exclusion, ca_exclusion, other_exlusion):
        self.exclusions = list()
        if loop_exclusion == "yes":
            self.exclusions.append(True)
        else:
            self.exclusions.append(False)
        if opiate_exclusion == "yes":
            self.exclusions.append(True)
        else:
            self.exclusions.append(False)
        if ca_exclusion == "yes":
            self.exclusions.append(True)
        else:
            self.exclusions.append(False)
        if other_exlusion == "yes":
            self.exclusions.append(True)
        else:
            self.exclusions.append(False)
        return

    def get_opiate_exclusion(self):
        return self.exclusions[0]

    def get_loop_exclusion(self):
        return self.exclusions[1]

    def get_ca_exclusion(self):
        return self.exclusions[2]

    def get_other_exclusion(self):
        return self.exclusions[3]

    def setPreOpDate(self, pre_op_date):
        self.Pre_Op_Date = pre_op_date
        return

    def getPreOpDate(self):
        return self.Pre_Op_Date

    def setPreOpCreat(self, pre_op_creat):
        self.Pre_Op_sCr = pre_op_creat
        return

    def getPreOpCreat(self):
        return self.Pre_Op_sCr

    def getStudyDOSTime(self):
        if (self.Bari_Surg_Date is not None) and (self.Diag_AHI_Date is not None):
            return (self.Bari_Surg_Date - self.Diag_AHI_Date).days
            # return relativedelta(self.Diag_AHI_Date, self.Bari_Surg_Date).years
        else:
            return None

    def getStudyDate(self):
        return self.Diag_AHI_Date

    def getDOB(self):
        return self.DOB

    def getDOS(self):
        return self.Bari_Surg_Date

    def getWeights(self):
        return self.Weights

    def getAgeAtDOS(self):
        return self.Age

    def setAHI(self, diag_ahi, diag_ahi_date):
        self.Diag_AHI = diag_ahi
        if type(diag_ahi_date) == type(""):
            self.Diag_AHI_Date = datetime.strptime(diag_ahi_date, '%m/%d/%Y')
        else:
            self.Diag_AHI_Date = diag_ahi_date

    def setBariDOS(self, surg_date):
        # Also sets age if DOB has been set
        self.Bari_Surg_Date = surg_date
        if self.DOB is None:
            return
        else:
            self.Age = relativedelta(surg_date, self.DOB).years

    def getEWL(self):
        if self.percExWtLossByTime is None:
            return [None, None, None, None, None, None, None, None, None]
        else:
            return self.percExWtLossByTime

    def setCCI(self, cci_string):
        self.CCI = cci_string

    def setHeight(self, height):
        """also sets excess weight loss by time if weights have already been set"""
        self.Height_DOS = height

    def setWeights(self, weights):
        """takes an array of weights, also calculated excess weight loss by time if height has also been set"""
        self.Weights = weights
        if self.Height_DOS is not None:
            self.percExWtLossByTime = self.calc_ewl_list(weights)

    def calc_weight_lost_list(self, weights):
        WL_list = list()
        if weights is not None:
            if weights[0] is not None:
                for i in range(len(weights)):
                    if weights[i] is not None:
                       WL_list.append(weights[i] - weights[0])
                    else:
                        weights.append(None)
        return WL_list


    def calc_ewl_list(self, weights):
        '''returns a list of Weight DOS - IBW (Devine formula)
        that the patient achieved
        ON HOLD UNTIL GENDER TAKEN FROM Db

        %EWL = (Preoperative Weight - Follow-up Weight)/(Preoperative Weight - Ideal Body Weight) * 100
        IBW = formally taken from MetLife Tables.
        '''
        if weights is None or len(weights) is 0 or weights[0] is None or self.Height_DOS is None or self.Sex is None:
            print("either weights, height, or sex not set")
            return None
        else:
            # print("all of weights, height, and sex set")
            IBW = 0
            perc_ewl_list = list()
            if self.Sex == "m":
                IBW = 50 + (0.9 * (self.Height_DOS - 152))
            else:
                IBW = 45.5 + (0.9 * (self.Height_DOS - 152))
            # print("IBW: "+str(IBW))
            # print("excess weight: " + str(weights[0] - IBW))
            self.IBW = IBW
            for i in range(len(weights)):
                if weights[i] is not None:
                    perc_ewl_list.append((weights[0] - weights[i]) / (weights[0] - IBW))
                else:
                    perc_ewl_list.append(None)
            return perc_ewl_list

    def getIBW(self):
        return self.IBW

    def getCCI(self):
        return self.CCI

    def weightDOS(self):
        try:
            return self.Weights[0]
        except (TypeError, ValueError):
            return None

    def setHCO3s(self, HCO3s_list):
        self.HCO3s = HCO3s_list
        delta_HCO3 = list()
        if HCO3s_list is not None:
            if HCO3s_list[0] is not None:
                for i in range(len(HCO3s_list)):
                    if HCO3s_list[i] is not None:
                        delta_HCO3.append(HCO3s_list[i] - HCO3s_list[0])
                    else:
                        delta_HCO3.append(None)
        self.HCO3ChangeSinceSurg = delta_HCO3

    def getHCO3s(self):
        return self.HCO3s

    def getDeltaHCO3s(self):
        if self.HCO3ChangeSinceSurg is None or len(self.HCO3ChangeSinceSurg) < 9:
            return [None, None, None, None, None, None, None, None, None]
        else:
            return self.HCO3ChangeSinceSurg

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

    def getMinHCO3(self):
        min_index = None
        min_HCO3 = 99  # above highest physiologic possibility
        for i in range(len(self.HCO3s)):
            if self.HCO3s[i] is not None:
                if self.HCO3s[i] <= min_HCO3:
                    min_HCO3 = self.HCO3s[i]
                    min_index = i
        if min_index is None:
            return None, None
        else:
            return min_index, min_HCO3

    def getMeanPostOpHCO3(self):
        num_measurements = 0
        total_HCO3 = 0
        for i in range(1, len(self.HCO3s)):
            if self.HCO3s[i] is not None:
                num_measurements += 1
                total_HCO3 += self.HCO3s[i]
        if num_measurements == 0:
            return None
        else:
            # print(self.HCO3s)
            # print(str(total_HCO3/num_measurements))
            return total_HCO3 / num_measurements

    def getMaxPostOpHCO3(self):
        max_index = None
        max_HCO3 = 0
        for i in range(1, len(self.HCO3s)):
            if self.HCO3s[i] is not None:
                if self.HCO3s[i] >= max_HCO3:
                    max_HCO3 = self.HCO3s[i]
                    max_index = i
        if max_index is None:
            return None, None
        else:
            return max_index, max_HCO3

    def all_hco3_below_25(self):
        '''returns true if all POST-OP values of HCO3 are below 25'''
        max_index, max_hco3 = self.getMaxPostOpHCO3()
        if max_index is None:
            return None
        if max_hco3 >= 25:
            return False
        else:
            return True

    def BMIDOS(self):
        return self.BMI_at_time(0)

    def BMI_at_time(self, index):
        """ weight (kg) / height(m)^2.
        [DOS, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y]. Kgs"""
        if len(self.Weights) > 0 and self.Weights[index] is not None:
            if self.Height_DOS is not None:
                return self.Weights[index] / ((float(self.Height_DOS)/100) ** 2)
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

    def percentWeightLoss(self):
        '''returns maximum weight loss as a percentage of weight at DOS'''
        if len(self.Weights) is 0 or self.Weights[0] is None:
            return None
        else:
            min = self.Weights[0]
            for weight in self.Weights:
                if weight is not None and weight < min:
                    min = weight
            return (1.0 - (min / self.Weights[0]))*100


    def lastWeightTime(self):
        '''returns the number of months since surgery of the last recorded
        weight'''
        months_since = {0: 0, 1: 2, 2: 4, 3: 6, 4: 12, 5: 24, 6: 36, 7: 48, 8: 60}
        for i in range(len(self.Weights)-1, 0, -1):  # update dic if wt len change
            if self.Weights[i] is not None:
                return months_since[i]
        return 0

    def getLastWeight(self):
        '''returns the last weight recorded'''
        for i in range(len(self.Weights)-1, 0, -1):  # update dic if wt len change
            if self.Weights[i] is not None:
                return self.Weights[i]
        return self.weightDOS()

    def getSex(self):
        return self.Sex

    def getMinWeight(self):
        '''returns the lowest weight'''
        min = 9999  # larger than largest
        for weight in self.Weights:
            if weight is not None and weight < min:
                min = weight
        return min

    def minWeightTime(self):
        '''returns the time (in months) of the minimum recorded weight'''
        min = 9999  # larger than largest
        min_i = 0
        months_since = {0: 0, 1: 2, 2: 4, 3: 6, 4: 12, 5: 24, 6: 36, 7: 48, 8: 60}
        for i in range(len(self.Weights)):  # update dic if wt len change
            if self.Weights[i] is not None and self.Weights[i] < min:
                min = self.Weights[i]
                min_i = i
        return months_since[min_i]

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
        print("DOB: " + str(self.DOB) + ", Age (days) @ Surgery: " + str(self.Age))
        print("DOS:" + str(self.Bari_Surg_Date) + " @ BMI: "
                + str(self.BMIDOS()))
        print("Charlson Comorbidity Index: "+ str(self.CCI))
        print("Height:" + str(self.Height_DOS))
        print("Weights: " + str(self.Weights))
        print("Ideal Body Weight: " + str(self.IBW))
        print("Perc. EBWL by time: " + str(self.percExWtLossByTime))
        print("HCO3s: " + str(self.HCO3s))
        print("Delta HCO3s: " + str(self.HCO3ChangeSinceSurg))
        print("Diagnostic AHI: " + str(self.Diag_AHI)
                + " on " + str(self.Diag_AHI_Date))
        print("Total of " + str(len(self.Compliance_Records))
                + " compliance records")
        for i in self.Compliance_Records:
            i.printCompRecord()
        print("Avg 4h+ compliance: " + str(self.avgCompliance()))
        print("Based on " + str(self.numDaysComplianceRecords())
                + " days of records")


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
        print(str(self.date) + ": Used 4+ h on " + str(self.days_used_4h)
            + "% of last " + str (self.days) + " days")
