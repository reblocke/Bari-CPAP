import pandas as pd
from RecordsDb import *
from AccessDb import AccessDatabase
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


# Locations
dbLoc = "/Users/reblocke/Box/Residency Personal Files/Scholarly Work/Bariatric CPAP Project/Bariatric Clinic data/"
compliance_dbLoc = "BARI_SLEEP_CPAP_COMPLIANCE_092619.xlsx"
outcome_dbLoc = "BARI_SLEEP_031919 from EDW - edits.xlsx"
compliance_data_sheet = "Sheet 1"
outcome_data_sheet = "Sheet 1"


def ComplianceVsWeightRegain(df):
    plt.style.use('seaborn-whitegrid')
    fig = plt.figure() # container object
    ax = plt.axes() #the box we'll draw in

    compliantPt = df[df['Avg Compliance'] > 0.0]
    noCompliantPt = df[df['Avg Compliance'] == 0.0]

    ax.scatter(compliantPt['Avg Compliance'], compliantPt['Weight Regain'],
        s= compliantPt['Days Comp Records'], alpha = 0.5,
        c="blue", label="Patients with CPAP compliance data")
    ax.scatter(noCompliantPt['Avg Compliance'], noCompliantPt['Weight Regain'],
        alpha = 0.5, c="red", marker='x',
        label="Patients without CPAP compliance data")

    ax.axis('tight')
    ax.set_title("PAP Compliance vs Weight Regain")
    ax.set_xlabel("Avg Compliance % of days 4+h. Size = # of days averaged")
    ax.set_ylabel("Weight Regain (Kg)")
    ax.legend(fancybox=True, framealpha=.75, shadow=True, borderpad=1)

    fig.savefig('Weight Regain vs Adherence')
    plt.show()  # only invoke 1 time per script


def RegainHistogramsCompliance(df):
    plt.style.use('ggplot')
    fig = plt.figure() # container object
    ax = plt.axes() #the box we'll draw in

    compliantPt = df[df['Avg Compliance'] > 0.0]
    ax.hist(compliantPt['Weight Regain'], bins=20, alpha=0.35, normed=True,
        histtype='barstacked', label="Patients with >0 CPAP Adherence",
        color='green')

    noCompliantPt = df[df['Avg Compliance'] == 0.0]
    ax.hist(noCompliantPt['Weight Regain'], bins=20, alpha=0.35, normed=True,
        histtype='barstacked', label="Patients with no CPAP Adherence",
        color='blue')

    ax.set_title("Histograms of Weight Regain")
    ax.set_xlabel("Weight Regain (Kg)")
    ax.set_ylabel("Percentage of patients")
    ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)

    fig.savefig('regainHist.png')
    plt.show()  # only invoke 1 time per script


def weightRegainBMI(df):
    g = sns.jointplot(x='BMI', y='Max Weight Loss', data=df)
    plt.show()

def compareCompVsNotWR(df):
    compliantPt = df[df['Avg Compliance'] > 0.0]
    noCompliantPt = df[df['Avg Compliance'] == 0.0]

    compliantPt.reset_index(inplace=True)
    noCompliantPt.reset_index(inplace=True)
    # Can't use independent T-test as variances are not homogenous
    # print(stats.levene(compliantPt['Weight Regain'], noCompliantPt['Weight Regain']))
    # Can't use tests assuming normality
    # print(stats.shapiro(compliantPt['Weight Regain']))
    # Unequal datset size?

    pass

def weightLossAndRegainVsAHI(df):
    sns.set()
    colors = ["Red", "Blue"]
    sns.set_palette(colors)
    sns.set_style("whitegrid")
    AHIdf = df[df['Diag AHI'].notnull()]
    f, axs = plt.subplots(2)
    f.suptitle("Maximum Weight Loss and Weight Regain vs Diagnostic AHI")
    sns.regplot(x='Diag AHI', y='Weight Regain', data=AHIdf, ax=axs[1])
    sns.regplot(x='Diag AHI', y='Max Weight Loss', data=AHIdf, ax=axs[0])
    axs[0].set_xlabel("Diagnostic AHI (events/hr)")
    axs[0].set_ylabel("Maximum Weight Loss (kg)")
    axs[1].set_xlabel("Diagnostic AHI (events/hr)")
    axs[1].set_ylabel("Weight Regain (kg)")

    #sns.boxplot(y='Weight Regain', data=noCompliantPt)
    #g = sns.jointplot(x='BMI', y='Max Weight Loss', data=df)
    #g.set_title("BMI vs Maximum Weight Loss Achieved")
    plt.tight_layout()
    plt.savefig("WLandWR_kg_vs_DiagAHI.png")

def visualizations(df):
    sns.set()
    plt.show()  # only invoke 1 time per script


def main():
    database = AccessDatabase(dbLoc, compliance_dbLoc, compliance_data_sheet,
        outcome_dbLoc, outcome_data_sheet)

    df = database.createDataFrame()

    print("\nWeight On Day of Surgery (Kg):")
    print(database.WeightDOSList().describe())

    print("\nWeight Loss Acheived (Kg):")
    print(database.WeightLossList().describe())

    print("\nWeight Regain Observed (Kg):")
    print(database.WeightRegainList().describe())

    # Print Stats for the subset with compliance data and without
    print("\nThose w/ compliance data")
    print(df[df['Avg Compliance'] > 0.0].describe())
    print("\nthose w/o compliance data")
    print(df[df['Avg Compliance'] == 0.0].describe())

    # Print Stats for the subset with a diagnostic AHI
    print("\nThose w/ diagnostic AHI")
    print(df[df['Diag AHI'].notnull()].describe())

    df.to_excel('output.xlsx')
    visualizations(df)

    # RegainHistogramsCompliance(df)
    # ComplianceVsWeightRegain(df)




if __name__ == '__main__':
    main()
