import pandas as pd
from RecordsDb import *
from AccessDb import AccessDatabase
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.patches as mpatches
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.sandbox.regression.predstd import wls_prediction_std

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
    plt.savefig("WLandWR_kg_vs_DiagAHI_FinalDb.jpg")


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

def weightDOSMinLastByPap(df):
    sns.set()
    sns.set_style("white")
    fig, axs = plt.subplots(1,11, sharey='row')

    comp_df = df[df['Avg Compliance'] > 0.0]
    no_comp_df = df[df['Avg Compliance'] == 0.0]

    sns.boxplot(y='DOS Weight', data = df, ax=axs[0], color='green')
    axs[0].set_ylabel("Weight in Kg")
    #axs[0].set_xlabel("DOS, All")
    sns.boxplot(y='DOS Weight', data = comp_df, ax=axs[1], color='blue')
    axs[1].set_ylabel("")
    axs[1].set_xlabel("Weight At Surgery\n(t=0 months)")
    sns.boxplot(y='DOS Weight', data = no_comp_df, ax=axs[2], color='yellow')
    axs[2].set_ylabel("")
    axs[2].label = "No Compliance"
    axs[3].set_visible(False)
    sns.boxplot(y='Min Weight', data = df, ax=axs[4], color='green')
    axs[4].set_ylabel("")
    sns.boxplot(y='Min Weight', data = comp_df, ax=axs[5], color='blue')
    axs[5].set_ylabel("")
    axs[5].set_xlabel("Weight Nadir\n(16.8 +/-12.7 months)")
    sns.boxplot(y='Min Weight', data = no_comp_df, ax=axs[6], color='yellow')
    axs[6].set_ylabel("")
    axs[7].set_visible(False)
    sns.boxplot(y='Last Weight', data = df, ax=axs[8], color='green')
    axs[8].set_ylabel("")
    sns.boxplot(y='Last Weight', data = comp_df, ax=axs[9], color='blue')
    axs[9].set_ylabel("")
    axs[9].set_xlabel("Last Recorded Weight\n(36.1 +/-16.5 months)")
    sns.boxplot(y='Last Weight', data = no_comp_df, ax=axs[10], color='yellow')
    axs[10].set_ylabel("")

    sns.despine(top=True, right=True, left=True, bottom=True)
    fig.suptitle("Weight Loss and Regain in CPAP Users and Nonusers")

    green_patch = mpatches.Patch(edgecolor='black', facecolor='green', label='All Patients (n='+str(len(df))+')')
    yellow_patch = mpatches.Patch(edgecolor='black', facecolor='yellow', label='Patients with no CPAP use (n='+str(len(no_comp_df))+')')
    blue_patch = mpatches.Patch(edgecolor='black', facecolor='blue', label='Patients with any CPAP use (n='+str(len(comp_df))+')')

    plt.legend(handles=[green_patch, blue_patch, yellow_patch])
    #plt.tight_layout()


def visualizations(df):
    weightDOSMinLastByPap(df)
    #weightLossAndRegainVsAHI(df)
    #lastWtWR(df)
    #RegainHistogramsCompliance(df)
    #ComplianceVsWeightRegain(df)
    plt.show()  # only invoke 1 time per script

def compareComplianceWR(df):
    comp_df = df[df['Avg Compliance'] > 0.0]
    no_comp_df = df[df['Avg Compliance'] == 0.0]
    print(stats.ttest_ind(comp_df['Weight Regain'].get_values(),no_comp_df['Weight Regain'].get_values(), equal_var=False))
    print(stats.mannwhitneyu(comp_df['Weight Regain'].get_values(),no_comp_df['Weight Regain'].get_values(), alternative='two-sided'))

def partialRegressionWt(df):
    pass


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
    final_df.to_excel('final output.xlsx')
    compareComplianceWR(final_df)
    visualizations(final_df)

    # RegainHistogramsCompliance(df)
    # ComplianceVsWeightRegain(df)




if __name__ == '__main__':
    main()
