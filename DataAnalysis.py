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
dbLoc = "/Users/reblocke/Box Sync/Residency Personal Files/Scholarly Work/Locke Research Projects/HCO3 in Bariatric Surgery/databases/Working/"
compliance_dbLoc = "BARI_SLEEP_CPAP_COMPLIANCE_092619.xlsx"
outcome_dbLoc = "Bari HCO3 10-30-21-working.xlsx"
compliance_data_sheet = "Sheet 1"
outcome_data_sheet = "Sheet 1"

# Data visualization utilities


def display_dist(df, label, subset="Full Cohort", lim_zero = True):
    # TODO: separate label from title argument to allow customization
    """takes a df and a column label and graphs the distribution (continuous) for display
    subset = label to include if the df passed to the function only contains part of the overall cohort
    lim_zero = true means that 0 should be included as the reference point on the x scale, negative values won't be shown.
    If not, the scale will be assumed to be interval (scales won't be limited to include 0)"""

    # TODO: ensure the height of the box plot is correct

    sns.set(style="white", palette="pastel")
    fig, axes = plt.subplots(2, 1, figsize=(9, 6))
    axes[1].set_aspect(aspect=1)

    # TODO: switch this to displot
    sns.distplot(df[label], ax=axes[0], kde=False, norm_hist=False, color='teal')
    sns.boxplot(data=df, x=label, ax=axes[1], color='skyblue')

    sns.despine(ax=axes[0], top=True, bottom=True, right=True)
    sns.despine(ax=axes[1], top=True, left=True, right=True)

    axes[0].set_xlabel("")
    axes[0].set_ylabel("Count per bin", fontsize='large')

    row_label = "{cohort}\n{lab}\nMean: {mean:.1f}, Std Dev: {std:.1f}\nMedian: {med:.1f}, IQR: [{lower:.1f}, {upper:.1f}]\nCount: {count:.0f}"\
        .format(cohort=subset, lab=label, mean=df[label].describe()['mean'], std=df[label].describe()['std'],
                med=df[label].describe()['50%'], lower=df[label].describe()['25%'], upper=df[label].describe()['75%'],
                count=df[label].describe()['count'])

    axes[1].set_xlabel(row_label, fontsize='medium')
    axes[1].get_shared_x_axes().join(axes[1], axes[0])
    if lim_zero:
        axes[1].set(xlim=(0, None))

    fig.suptitle("Distribution of: " + str(label) + " in " + str(subset), fontsize='x-large')
    fig.tight_layout(rect=[0, 0, 1, .9])  # .95 to leave space for title
    fig.savefig('dist figs/Display Dist ' + str(label) + "-"+ str(subset) +'.png', dpi=100)
    plt.close()


def display_cats(df, label, subset="Full Cohort"):
    # TODO: separate label from title argument to allow customization
    """takes a df and a column label and graphs the counts of categories for display"""
    sns.set(style="white", palette="cubehelix")
    fig, axes = plt.subplots(2, 1, figsize=(9, 6))

    sns.histplot(df[label].dropna(), ax=axes[0])
    counts = df[label].value_counts()
    axes[1].pie(counts, labels=counts.index)
    axes[1].text(-3.0, -1.3, "Value counts:\n\n"+str(counts) + "\n" + str(subset), fontsize=10)

    sns.despine(ax=axes[0], top=True, bottom=True, right=True, left=True)
    axes[0].set_xlabel("")

    fig.suptitle("Distribution of: " + str(label) + " in " + str(subset), fontsize='xx-large')
    # fig.tight_layout(rect=[0, 0, 1, .9])  # .95 to leave space for title
    fig.savefig('dist figs/Display Cat ' + str(label) + "-"+ str(subset) + '.png', dpi=100)
    plt.close()


#Visualizations

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
    ax.hist(compliantPt['Weight Regain'], bins=20, alpha=0.35, density=True,
        histtype='barstacked', label="Patients with >0 CPAP Adherence",
        color='green')

    noCompliantPt = df[df['Avg Compliance'] == 0.0]
    ax.hist(noCompliantPt['Weight Regain'], bins=20, alpha=0.35, density=True,
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


    print("Hi")
    # Unequal datset size?

    pass


def weightLossAndRegainVsAHI(df):
    sns.set()
    sns.set_style("whitegrid")
    AHIdf = df[df['Diag AHI'].notnull()]
    f, axs = plt.subplots(2, figsize=(5,5))
    f.suptitle("Maximum Weight Loss and Regain vs OSA Severity", fontsize=14)

    # If partial regression controlling for last weight time is desired.
    #sns.regplot(x='Diag AHI', y='Weight Regain', y_partial='Last Weight Time', data=AHIdf, ax=axs[1], color='r')
    #sns.regplot(x='Diag AHI', y='Max Weight Loss Pct', y_partial='Last Weight Time', data=AHIdf, ax=axs[0], color='b')

    sns.regplot(x='Diag AHI', y='Max Weight Loss Pct', data=AHIdf, ax=axs[0], color='darkgreen')
    sns.regplot(x='Diag AHI', y='Weight Regain', data=AHIdf, ax=axs[1], color='darkred')

    # above now includes partial regression on last weight time, which does not appear to make all that much difference.

    axs[0].set_xlabel("Diagnostic AHI (events/hr)")
    axs[0].set_ylabel("Maximum Weight Loss\n(%Weight DOS)")
    axs[1].set_xlabel("Diagnostic AHI (events/hr)")
    axs[1].set_ylabel("Weight Regain (kg)\n(Max weight - weight nadir)")

    f.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("figure_2_transparent.png", transparent=True)


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
    sns.swarmplot(y='DOS Weight', data = df, ax=axs[0], color='black', size=3)
    axs[0].set_ylabel("Weight in Kg")
    #axs[0].set_xlabel("DOS, All")
    sns.boxplot(y='DOS Weight', data = comp_df, ax=axs[1], color='blue')
    sns.swarmplot(y='DOS Weight', data = comp_df, ax=axs[1], color='black', size=3)
    axs[1].set_ylabel("")
    axs[1].set_xlabel("Weight At Surgery\n(t=0 months)")
    sns.boxplot(y='DOS Weight', data = no_comp_df, ax=axs[2], color='yellow')
    sns.swarmplot(y='DOS Weight', data = no_comp_df, ax=axs[2], color='black', size=3)
    axs[2].set_ylabel("")
    axs[2].label = "No Compliance"
    axs[3].set_visible(False)
    sns.boxplot(y='Min Weight', data = df, ax=axs[4], color='green')
    sns.swarmplot(y='Min Weight', data = df, ax=axs[4], color='black', size=3)
    axs[4].set_ylabel("")
    sns.boxplot(y='Min Weight', data = comp_df, ax=axs[5], color='blue')
    sns.swarmplot(y='Min Weight', data = comp_df, ax=axs[5], color='black', size=3)
    axs[5].set_ylabel("")
    axs[5].set_xlabel("Weight Nadir\n(16.8 +/-12.7 months)")
    sns.boxplot(y='Min Weight', data = no_comp_df, ax=axs[6], color='yellow')
    sns.swarmplot(y='Min Weight', data = no_comp_df, ax=axs[6], color='black', size=3)
    axs[6].set_ylabel("")
    axs[7].set_visible(False)
    sns.boxplot(y='Last Weight', data = df, ax=axs[8], color='green')
    sns.swarmplot(y='Last Weight', data = df, ax=axs[8], color='black', size=3)
    axs[8].set_ylabel("")
    sns.boxplot(y='Last Weight', data = comp_df, ax=axs[9], color='blue')
    sns.swarmplot(y='Last Weight', data = comp_df, ax=axs[9], color='black', size=3)
    axs[9].set_ylabel("")
    axs[9].set_xlabel("Last Recorded Weight\n(36.1 +/-16.5 months)")
    sns.boxplot(y='Last Weight', data = no_comp_df, ax=axs[10], color='yellow')
    sns.swarmplot(y='Last Weight', data = no_comp_df, ax=axs[10], color='black', size=3)
    axs[10].set_ylabel("")

    sns.despine(top=True, right=True, left=True, bottom=True)
    fig.suptitle("Weight Loss and Regain in CPAP Users and Nonusers")

    green_patch = mpatches.Patch(edgecolor='black', facecolor='green', label='All Patients (n='+str(len(df))+')')
    yellow_patch = mpatches.Patch(edgecolor='black', facecolor='yellow', label='Patients with no CPAP use (n='+str(len(no_comp_df))+')')
    blue_patch = mpatches.Patch(edgecolor='black', facecolor='blue', label='Patients with any CPAP use (n='+str(len(comp_df))+')')

    fig.legend(handles=[green_patch, blue_patch, yellow_patch], loc='center', bbox_to_anchor=(0.5, 0.2), framealpha=0)
    plt.ylim(0,200)
    #plt.tight_layout()
    fig.savefig('figure_1_transparent.png', transparent=True)

def delta_hco3_trajectory(df):
    sns.set()
    sns.set_style("white")
    fig, axs = plt.subplots(1,11, sharey='row')

    comp_df = df[df['Avg Compliance'] > 0.0]
    no_comp_df = df[df['Avg Compliance'] == 0.0]

    sns.boxplot(y='6mo Delta HCO3', data = df, ax=axs[0], color='green')
    sns.swarmplot(y='6mo Delta HCO3', data = df, ax=axs[0], color='black', size=3)
    axs[0].set_ylabel("Change in [HCO3-] (mEq/L) Since Surgery")
    axs[0].axhline(y=0, color='red', linestyle="-", linewidth=2.5, label="Pre-op [HCO3-]")
    #axs[0].set_xlabel("DOS, All")
    sns.boxplot(y='6mo Delta HCO3', data = comp_df, ax=axs[1], color='blue')
    sns.swarmplot(y='6mo Delta HCO3', data = comp_df, ax=axs[1], color='black', size=3)
    axs[1].set_ylabel("")
    axs[1].set_xlabel("6 months after surgery")
    axs[1].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    sns.boxplot(y='6mo Delta HCO3', data = no_comp_df, ax=axs[2], color='yellow')
    sns.swarmplot(y='6mo Delta HCO3', data = no_comp_df, ax=axs[2], color='black', size=3)
    axs[2].set_ylabel("")
    axs[2].label = "No Compliance"
    axs[2].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    # axs[3].set_visible(False)
    axs[3].xaxis.set_ticklabels([])
    axs[3].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    sns.boxplot(y='1y Delta HCO3', data = df, ax=axs[4], color='green')
    sns.swarmplot(y='1y Delta HCO3', data = df, ax=axs[4], color='black', size=3)
    axs[4].set_ylabel("")
    axs[4].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    sns.boxplot(y='1y Delta HCO3', data = comp_df, ax=axs[5], color='blue')
    sns.swarmplot(y='1y Delta HCO3', data = comp_df, ax=axs[5], color='black', size=3)
    axs[5].set_ylabel("")
    axs[5].set_xlabel("1 year after surgery")
    axs[5].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    sns.boxplot(y='1y Delta HCO3', data = no_comp_df, ax=axs[6], color='yellow')
    sns.swarmplot(y='1y Delta HCO3', data = no_comp_df, ax=axs[6], color='black', size=3)
    axs[6].set_ylabel("")
    axs[6].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    # axs[7].set_visible(False)
    axs[7].xaxis.set_ticklabels([])
    axs[7].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    sns.boxplot(y='2y Delta HCO3', data = df, ax=axs[8], color='green')
    sns.swarmplot(y='2y Delta HCO3', data = df, ax=axs[8], color='black', size=3)
    axs[8].set_ylabel("")
    axs[8].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    sns.boxplot(y='2y Delta HCO3', data = comp_df, ax=axs[9], color='blue')
    sns.swarmplot(y='2y Delta HCO3', data = comp_df, ax=axs[9], color='black', size=3)
    axs[9].set_ylabel("")
    axs[9].set_xlabel("2 years after surgery")
    axs[9].axhline(y=0, color='red', linestyle="-", linewidth=2.5)
    sns.boxplot(y='2y Delta HCO3', data = no_comp_df, ax=axs[10], color='yellow')
    sns.swarmplot(y='2y Delta HCO3', data = no_comp_df, ax=axs[10], color='black', size=3)
    axs[10].set_ylabel("")
    axs[10].axhline(y=0, color='red', linestyle="-", linewidth=2.5)

    sns.despine(top=True, right=True, left=True, bottom=True)
    fig.suptitle("Change in [HCO3-] in Patients At-Risk for OHS After Bariatric Surgery")

    green_patch = mpatches.Patch(edgecolor='black', facecolor='green', label='All patients (n='+str(len(df))+')')
    yellow_patch = mpatches.Patch(edgecolor='black', facecolor='yellow', label='Patients without pre-op CPAP use (n='+str(len(no_comp_df))+')')
    blue_patch = mpatches.Patch(edgecolor='black', facecolor='blue', label='Patients with pre-op CPAP use (n='+str(len(comp_df))+')')

    fig.legend(handles=[green_patch, blue_patch, yellow_patch], loc='center', bbox_to_anchor=(0.5, 0.2), framealpha=0)
    plt.ylim(-12,4)
    #plt.tight_layout()
    fig.savefig('figure_1_delta_HCO3.png', transparent=False)

def hco3_trajectory(df):
    # TODO: finish conversion
    # Do: stratify by: whole dataset, those with HCO3 over 25, those with HCO3 over 25 and CPAP adherence prior.
    # NOTE: requires WHOLE_DF, not just DF
    sns.set()
    sns.set_style("white")
    fig, axs = plt.subplots(1,15, sharey='row')

    at_risk_df = df[df['Pre Op HCO3'] >= 25.0]
    comp_df = at_risk_df[at_risk_df['Avg Compliance'] > 0.0]

    #sns.violinplot(y='Pre Op HCO3', data=df, ax=axs[0], color='green', scale="count", inner="quartile")
    sns.boxplot(y='Pre Op HCO3', data = df, ax=axs[0], color='green')
    # sns.swarmplot(y='Pre Op HCO3', data = df, ax=axs[0], color='black', size=2)
    axs[0].set_ylabel("[HCO3-] in mEq/L)")
    # axs[0].set_xlabel("DOS, All")
    axs[0].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[0].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[0].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='Pre Op HCO3', data = at_risk_df, ax=axs[1], color='blue', scale="count", inner="quartile")
    sns.boxplot(y='Pre Op HCO3', data=at_risk_df, ax=axs[1], color='blue')
    # sns.swarmplot(y='Pre Op HCO3', data = at_risk_df, ax=axs[1], color='black', size=2)
    axs[1].set_ylabel("")
    axs[1].set_xlabel("Before\nSurgery")
    axs[1].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[1].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[1].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='Pre Op HCO3', data = comp_df, ax=axs[2], color='yellow', scale="count", inner="quartile")
    sns.boxplot(y='Pre Op HCO3', data=comp_df, ax=axs[2], color='yellow')
    # sns.swarmplot(y='Pre Op HCO3', data = comp_df, ax=axs[2], color='black', size=2)
    axs[2].set_ylabel("")
    axs[2].label = "No Compliance"
    axs[2].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[2].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[2].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    axs[3].xaxis.set_ticklabels([])
    axs[3].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[3].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[3].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='6mo HCO3', data=df, ax=axs[4], color='green', scale="count", inner="quartile")
    sns.boxplot(y='6mo HCO3', data = df, ax=axs[4], color='green')
    # sns.swarmplot(y='6mo HCO3', data = df, ax=axs[4], color='black', size=2)
    axs[4].set_ylabel("")
    axs[4].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[4].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[4].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='6mo HCO3', data=at_risk_df, ax=axs[5], color='blue', scale="count", inner="quartile")
    sns.boxplot(y='6mo HCO3', data = at_risk_df, ax=axs[5], color='blue')
    # sns.swarmplot(y='6mo HCO3', data = at_risk_df, ax=axs[5], color='black', size=2)
    axs[5].set_ylabel("")
    axs[5].set_xlabel("6 months\n after surgery")
    axs[5].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[5].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[5].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='6mo HCO3', data=comp_df, ax=axs[6], color='yellow', scale="count", inner="quartile")
    sns.boxplot(y='6mo HCO3', data = comp_df, ax=axs[6], color='yellow')
    # sns.swarmplot(y='6mo HCO3', data = comp_df, ax=axs[6], color='black', size=2)
    axs[6].set_ylabel("")
    axs[6].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[6].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[6].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    axs[7].xaxis.set_ticklabels([])
    axs[7].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[7].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[7].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='1y HCO3', data=df, ax=axs[8], color='green', scale="count", inner="quartile")
    sns.boxplot(y='1y HCO3', data = df, ax=axs[8], color='green')
    # sns.swarmplot(y='1y HCO3', data = df, ax=axs[8], color='black', size=2)
    axs[8].set_ylabel("")
    axs[8].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[8].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[8].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='1y HCO3', data=at_risk_df, ax=axs[9], color='blue', scale="count", inner="quartile")
    sns.boxplot(y='1y HCO3', data = at_risk_df, ax=axs[9], color='blue')
    # sns.swarmplot(y='1y HCO3', data = at_risk_df, ax=axs[9], color='black', size=2)
    axs[9].set_ylabel("")
    axs[9].set_xlabel("1 year\nafter surgery")
    axs[9].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[9].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[9].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='1y HCO3', data=comp_df, ax=axs[10], color='yellow', scale="count", inner="quartile")
    sns.boxplot(y='1y HCO3', data = comp_df, ax=axs[10], color='yellow')
    # sns.swarmplot(y='1y HCO3', data = comp_df, ax=axs[10], color='black', size=2)
    axs[10].set_ylabel("")
    axs[10].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[10].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[10].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    axs[11].xaxis.set_ticklabels([])
    axs[11].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[11].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[11].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='2y HCO3', data=df, ax=axs[12], color='green', scale="count", inner="quartile")
    sns.boxplot(y='1y HCO3', data = df, ax=axs[12], color='green')
    # sns.swarmplot(y='1y HCO3', data = df, ax=axs[12], color='black', size=2)
    axs[12].set_ylabel("")
    axs[12].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[12].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[12].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='2y HCO3', data=at_risk_df, ax=axs[13], color='blue', scale="count", inner="quartile")
    sns.boxplot(y='1y HCO3', data = at_risk_df, ax=axs[13], color='blue')
    # sns.swarmplot(y='1y HCO3', data = at_risk_df, ax=axs[13], color='black', size=2)
    axs[13].set_ylabel("")
    axs[13].set_xlabel("2 years\nafter surgery")
    axs[13].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[13].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean")
    axs[13].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population Mean (4500ft)")
    # sns.violinplot(y='2y HCO3', data=comp_df, ax=axs[14], color='yellow', scale="count", inner="quartile")
    sns.boxplot(y='1y HCO3', data = comp_df, ax=axs[14], color='yellow')
    # sns.swarmplot(y='1y HCO3', data = comp_df, ax=axs[14], color='black', size=2)
    axs[14].set_ylabel("")
    axs[14].xaxis.set_ticklabels([])
    axs[14].axhline(y=25, color='grey', linestyle=":", linewidth=2.0, label="At Risk Threshold")
    axs[14].axhline(y=22.93, color='black', linestyle=":", linewidth=2.0, label="Sample Mean [HCO3-]")
    axs[14].axhline(y=21.8, color='purple', linestyle=":", linewidth=2.0, label="Expected Population\nMean [HCO3-] (4500ft)")

    sns.despine(top=True, right=True, left=True, bottom=True)
    fig.suptitle("[HCO3-] Change in Patients Undergoing Bariatric Surgery")
    axs[14].legend(bbox_to_anchor=(0, 0.05), loc='lower center', fontsize='xx-small')

    green_patch = mpatches.Patch(edgecolor='black', facecolor='green', label='All patients (n='+str(len(df))+')')
    blue_patch = mpatches.Patch(edgecolor='black', facecolor='blue',
                                label='At risk for OHS, [HCO3-] >= 25 mEq/L(n=' + str(
                                    len(at_risk_df)) + ')')
    yellow_patch = mpatches.Patch(edgecolor='black', facecolor='yellow', label='Pre-op CPAP use, still at risk for OHS (n='+str(len(comp_df))+')')
    fig.legend(handles=[green_patch, blue_patch, yellow_patch], loc='center', bbox_to_anchor=(0.4, 0.2), framealpha=0)

    plt.ylim(12,32)
    #plt.tight_layout()
    fig.savefig('figure_2_HCO3.png', transparent=False)
    plt.show()


def calc_percentiles_by_time(df, columns):
    """takes labels of the columns:
        either length 8 (not including day of surgery) or length 9 (including day of surgery)

        [DOS, +2mo, +4mo, +6mo, +1y, +2y, +3y, +4y, +5y]"""


def distributions(df):
    cohort_labels = ['Full Cohort', "w Sleep Test", "Adherent", "Non-adherent"]

    final_df = df[df['Diag AHI'].notnull()]  # filter out no diag ahi
    final_df = final_df[final_df['DOS Weight'].notnull()]  # filter no wt DOS
    # final_df = patients with a diagnostic AHI

    adh_df = final_df[final_df['Avg Compliance'] > 0.0]
    non_adh_df = final_df[final_df['Avg Compliance'] == 0.0]
    cohort_dfs = [df, final_df, adh_df, non_adh_df]

    for i in range(len(cohort_labels)):
        print(cohort_labels[i])
        display_dist(cohort_dfs[i], "Max Weight Loss Pct", subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "DOS Weight", subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "Min Weight", subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "Min Weight Time", subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "Last Weight Time", subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "Weight Regain", lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "Max Weight Loss", lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "Diag AHI", subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "Study Surgery Time", lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], 'Pre Op sCr', subset = cohort_labels[i])
        display_dist(cohort_dfs[i], "Avg Compliance", subset=cohort_labels[i])
        display_dist(cohort_dfs[i], "BMI", subset=cohort_labels[i])
        display_cats(cohort_dfs[i], 'Sex', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], 'Age at Surgery', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], 'CCI', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], 'DOS Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '2mo Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '4mo Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '6mo Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '1y Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '2y Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '3y Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '4y Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '5y Weight', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '2mo EWL', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '4mo EWL', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '6mo EWL', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '1y EWL', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '2y EWL', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '3y EWL', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '4y EWL', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '5y EWL', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], 'Weight Regain', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], 'BMI', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], 'Pre Op HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '2mo HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '4mo HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '6mo HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '1y HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '2y HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '3y HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '4y HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '5y HCO3', subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '2mo Delta HCO3', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '4mo Delta HCO3', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '6mo Delta HCO3', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '1y Delta HCO3', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '2y Delta HCO3', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '3y Delta HCO3', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '4y Delta HCO3', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], '5y Delta HCO3', lim_zero=False, subset=cohort_labels[i])
        display_dist(cohort_dfs[i], 'Days Comp Records', subset=cohort_labels[i])


def visualizations(df):
    #Distribution visualizations
    #Output figures
    #weightDOSMinLastByPap(df)
    #weightLossAndRegainVsAHI(df)
    #lastWtWR(df)
    #RegainHistogramsCompliance(df)
    #ComplianceVsWeightRegain(df)
    delta_hco3_trajectory(df)
    plt.show()  # only invoke 1 time per script


def compareComplianceWR(df):
    comp_df = df[df['Avg Compliance'] > 0.0]
    no_comp_df = df[df['Avg Compliance'] == 0.0]
    print("\nStatistical Test comparing weight regain (last - nadir) in patient with compliance data vs none")
    print(stats.ttest_ind(comp_df['Weight Regain'], no_comp_df['Weight Regain'], equal_var=False))
    print(stats.mannwhitneyu(comp_df['Weight Regain'], no_comp_df['Weight Regain'], alternative='two-sided'))


def main():
    database = AccessDatabase(dbLoc, compliance_dbLoc, compliance_data_sheet,
        outcome_dbLoc, outcome_data_sheet)

    # database.printDb()  #TODO: go through and check that these make sense
    df = database.createDataFrame()

    #print("\nWeight On Day of Surgery (Kg) - All Db:")
    #print(database.WeightDOSList().describe())

    print(df.describe()['MRN']['count'])
    df.to_excel('full_output.xlsx')
    print("\nExclude Patients w/ Loop Diuretic Use")
    df = df[df['Loop Exclusion'] == False]
    print(df.describe()['MRN']['count'])
    print("\nExclude Patients w/ chronic Opiate Use")
    df = df[df['Opiate Exclusion'] == False]
    print(df.describe()['MRN']['count'])
    print("\nExclude Patients w/ Carbonic Anhydrase inhibitor (e.g. Topiramate) Use")
    df = df[df['CA Exclusion'] == False]
    print(df.describe()['MRN']['count'])
    print("\nExclude Patients w/ other medication influencing acid/base status Use")
    df = df[df['Other Exclusion'] == False]
    print(df.describe()['MRN']['count'])
    print("\nExclude Patients without Pre-Op info")
    df = df[df['Pre Op sCr'].notnull()]
    print(df.describe()['MRN']['count'])
    print("\nExclude Patients without Post-Op HCO3 measurement")
    df = df[df['All HCO3 Below 25'].notnull()]
    print(df.describe()['MRN']['count'])
    print("\nExclude Patients with baseline sCr over 1.3")
    df = df[df['Pre Op sCr'] <= 1.3]
    print(df.describe()['MRN']['count'])

    df.describe().to_excel('whole_cohort_output_stats.xlsx')
    whole_df = df

    print("How many patients classified as at least 'At Risk' for OHS")
    df = df[df['Pre Op HCO3'] >= 25.0]  # 25 HCO3 cutoff given our elevation
    print(df.describe()['MRN']['count'])

    # Print Stats on entire db:
    print("\nEntire Database:")

    df.describe().to_excel('output_stats.xlsx')

    persistent_OHS_df = df[df['Mean HCO3 Post Op'] >= 25.0]
    persistent_OHS_df.describe().to_excel('persistent_OHS_output_stats.xlsx')
    OHS_resolved_df = df[df['Mean HCO3 Post Op'] < 25.0]
    OHS_resolved_df.describe().to_excel('OHS_resolved_output_stats.xlsx')
    print(stats.ttest_ind(OHS_resolved_df['Max Weight Loss'], persistent_OHS_df['Max Weight Loss'], equal_var=False))
    print(stats.ttest_ind(OHS_resolved_df['Weight Regain'], persistent_OHS_df['Weight Regain'], equal_var=False))
    # df = df[df['Diag AHI'].notnull()]  ## restrict to only patients with sleep apnea testing in our system
    # distributions(df)
    df.to_excel('output.xlsx')

    visualizations(df)
    hco3_trajectory(whole_df)

    #print("\nThose w/ diagnostic AHI")
    #final_df = df[df['Diag AHI'].notnull()]  # filter out no diag ahi
    # final_df = final_df[final_df['DOS Weight'].notnull()]  # filter no wt DOS
    #print(final_df.describe())
    #final_df.describe().to_excel('Describe Final Df.xlsx')

    # Print Stats for the subset with compliance data and without
    #print("\nThose w/ compliance + Dx AHI")
    #print(final_df[final_df['Avg Compliance'] > 0.0].describe())
    #final_df[final_df['Avg Compliance'] > 0.0].describe().to_excel('Describe Final Df w Comp.xlsx')

    #print("\nthose w/o compliance (0 or no data)+ Dx AHI")
    #print(final_df[final_df['Avg Compliance'] == 0.0].describe())
    #final_df[final_df['Avg Compliance'] == 0.0].describe().to_excel('Describe Final Df wo Comp.xlsx')

    #Statistical tests
    #compareComplianceWR(df)
    #final_df.to_excel('final output.xlsx')


if __name__ == '__main__':
    main()
