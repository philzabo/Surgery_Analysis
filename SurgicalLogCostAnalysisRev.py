import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

########## METAPARAMETERS ##########
file = 'surg_full.csv' #source file name
procs = ['ROBO 040','GEN 164','GEN 084','PEDS 218','PEDS 282'] #proc codes for focus
min_vol = 5 #min number of cases that a surgeon need to be included
group_param = 'CASE_SURGEON' #feature for grouping cases
cost1, cost2 = 'TX_COST','SUP_COST' #cost types to be compared
param1, param2 = 'TIME_REQUIRED','PAT_AGE' #other features to compare for correlation
####################################

# Load data, subset to relevant procs, sum by costs, crop out cases where surgeon has done under a certain count threshold
df_full = pd.read_csv(file)
df_full = df_full[df_full['PROC_ID'].isin(procs)]
df = df_full[['LOG_ID','PROC_ID','PROC_NAME','CASE_SURGEON','SUP_COST','TX_COST','PAT_AGE','TIME_REQUIRED']]
df = df.groupby(['LOG_ID','PROC_ID','PROC_NAME','CASE_SURGEON','PAT_AGE','TIME_REQUIRED']).sum().reset_index()
df = df.groupby(group_param).filter(lambda x : len(x)>min_vol)

# Output basic Stats
df_stats = df[[cost1, cost2]]
df_stats = df_stats.describe(include=['number'])
df_stats.to_csv('Surg_Stats.csv', index=True)

# Graphing functions
def plot_box_w_dist(data,value,num):
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
    # Add a graph in each part - graph SUP cost
    sns.boxplot(data[value], ax=ax_box)
    sns.distplot(data[value], ax=ax_hist)
    # Remove x axis name for the boxplot
    ax_box.set(xlabel='')
    plt.savefig('('+str(num)+')'+str(value)+'-All.png')
    plt.gcf().clear()
    num +=1
    return num

def plot_violin(data,value,split,num):
    # Setup violin plot on SUP cost by surgeon
    v_plot = sns.violinplot(y=value, x=split, data=data, width=0.5, palette="colorblind",
                              cut=0)  # , inner="stick")
    # add swarmplot - good check for actual distributions
    #sup_plot = sns.swarmplot(y='SUP_COST', x='CASE_SURGEON', data=df, color='black', alpha=0.75)
    # Add SUP cost violin plot attributes & labels
    v_plot.axes.set_title("", fontsize=16)
    v_plot.set_xlabel(split, fontsize=14)
    v_plot.set_ylabel(value, fontsize=14)
    v_plot.tick_params(labelsize=10)
    v_plot.set_xticklabels(v_plot.get_xticklabels(), rotation=30)
    plt.tight_layout()
    plt.savefig('('+str(num)+')'+str(value)+' by '+str(split)+'.png')
    plt.gcf().clear()
    num += 1
    return num

def plot_scatter(data,x,y,z,num):
    sns.set_context("notebook", font_scale=1.1)
    sns.set_style("ticks")
    # Create scatterplot of dataframe
    sns.lmplot(x,  # Horizontal axis
               y,  # Vertical axis
               data=data,  # Data source
               fit_reg=False,  # Don't fix a regression line
               hue=z,  # Set color
               scatter_kws={"marker": "D",  # Set marker style
                            "s": 100})  # S marker size
    # Set title
    plt.title(str(y) + ' vs ' + str(x))
    # Set x-axis label
    plt.xlabel(x)
    # Set y-axis label
    plt.ylabel(y)
    plt.savefig('('+str(num)+')'+str(y) + '_v_' + str(x) + '.png')
    plt.gcf().clear()
    num += 1
    return num

# num iterates on each function call & is returned, numbering the final picture files
num = 1
num = plot_box_w_dist(df,cost1,num)
num = plot_box_w_dist(df,cost2,num)
num = plot_violin(df,cost1,group_param,num)
num = plot_violin(df,cost2,group_param,num)
num = plot_scatter(df,param2,param1,group_param,num)
num = plot_scatter(df,param2,cost2,group_param,num)
num = plot_scatter(df,param1,cost2,group_param,num)
