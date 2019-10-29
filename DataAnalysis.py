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

    fig.savefig('regainHist_final.png')
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

    # Can't use tests assuming normality (=need non-parametric test)
    # print(stats.shapiro(compliantPt['Weight Regain']))


    # Unequal datset size?

    pass

def weightLossAndRegainVsAHI(df):
    sns.set()
    xkcd = ['#c04e01', "#980002"]
    sns.set_palette(xkcd)
    #sns.set_style("whitegrid")
    AHIdf = df[df['Diag AHI'].notnull()]
    f, axs = plt.subplots(2)
    f.suptitle("Maximum Weight Loss and Weight Regain vs Diagnostic AHI")
    sns.regplot(x='Diag AHI', y='Weight Regain', data=AHIdf, ax=axs[0])
    sns.regplot(x='Diag AHI', y='Max Weight Loss Pct', data=AHIdf, ax=axs[1])
    axs[0].set_xlabel("Diagnostic AHI (events/hr)")
    axs[0].set_ylabel("Weight Regain (kg)")
    axs[1].set_xlabel("Diagnostic AHI (events/hr)")
    axs[1].set_ylabel("Maximum Weight Loss\n(%Weight DOS)")

    # TODO: INCLUDE PARTIAL REGRESSION ON TIME OF LAST WEIGHT REGAIN
    # Appears the regplot partial regression call is broken.

    f.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("WLandWR_kg_vs_DiagAHI_FinalDb.png")


def lastWtWR(df):
    sns.set()
    ax = sns.regplot(x='Last Weight Time', y='Weight Regain', data=df)
    ax.set_xlabel("Months since bariatric surgery of LAST recorded weight")
    ax.set_ylabel("Weight Regain (Kg)")
    plt.title("Influence of Last Weight Recorded vs Weight Regain")
    # This shows that time for last recorded weight is a possible confounder-
    # and is almost certainly given that compliance to CPAP => more likely
    # later weights
    plt.show()  # only invoke 1 time per script


def visualizations(df):
    sns.set()
    #weightLossAndRegainVsAHI(df)
    #lastWtWR(df)
    #RegainHistogramsCompliance(df)
    #ComplianceVsWeightRegain(df)


    # 3 data points = weight DOS, min weight, last weight



    plt.show()  # only invoke 1 time per script


def main():
    database = AccessDatabase(dbLoc, compliance_dbLoc, compliance_data_sheet,
        outcome_dbLoc, outcome_data_sheet)

    df = database.createDataFrame()

    print("\nWeight On Day of Surgery (Kg) - All Db:")
    print(database.WeightDOSList().describe())


    #Print Stats on entire db:
    print("\nEntire Database:")
    print(df.describe())

    print("\nThose w/ diagnostic AHI")
    final_df = df[df['Diag AHI'].notnull()]  # filter out no diag ahi
    final_df = final_df[final_df['DOS Weight'].notnull()]  # filter no wt DOS
    #print(final_df.describe())
    final_df.describe().to_excel('Describe Final Df.xlsx')

    # Print Stats for the subset with compliance data and without
    print("\nThose w/ compliance + Dx AHI")
    #print(final_df[final_df['Avg Compliance'] > 0.0].describe())
    final_df[final_df['Avg Compliance'] > 0.0].describe().to_excel('Describe Final Df w Comp.xlsx')

    print("\nthose w/o compliance (0 or no data)+ Dx AHI")
    #print(final_df[final_df['Avg Compliance'] == 0.0].describe())
    final_df[final_df['Avg Compliance'] == 0.0].describe().to_excel('Describe Final Df wo Comp.xlsx')

    df.to_excel('output.xlsx')
    visualizations(final_df)

    # RegainHistogramsCompliance(df)
    # ComplianceVsWeightRegain(df)




if __name__ == '__main__':
    main()
