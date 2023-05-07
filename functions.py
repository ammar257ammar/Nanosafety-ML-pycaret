import pandas as pd
import numpy as np
import scipy
import math
import os

import seaborn as sns                       #visualisation
import matplotlib.pyplot as plt             #visualisation

# Managing Warnings
import warnings
warnings.filterwarnings('ignore')

import sklearn
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.impute import SimpleImputer

def plot_distribution(dataset):

    plt.style.use('seaborn-whitegrid')
    fig = plt.figure(figsize=(20,30))
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.5)

    rows = math.ceil(float(dataset.shape[1]) / 3)

    for i, column in enumerate(dataset.columns):

        ax = fig.add_subplot(rows, 3, i + 1)
        ax.set_title(column)

        if dataset.dtypes[column] == np.object:

            if(len(dataset[column].unique()) > 10):

                most_frequent = dataset[column].value_counts().sort_values(ascending=False)[:10].index.tolist()
                g = sns.countplot(y=column, data=dataset[dataset[column].isin(most_frequent)])
                ax.set_title(column + " (10 out of " + str(len(dataset[column].unique())) + " most frequent values)")
            else:
                g = sns.countplot(y=column, data=dataset)

            substrings = [s.get_text()[:18] for s in g.get_yticklabels()]
            g.set(yticklabels=substrings)
            plt.xticks(rotation=25)
        else:
            g = sns.distplot(dataset[column])
            plt.xticks(rotation=25)

def plot_distribution_train_test(train, test):

    plt.style.use('seaborn-whitegrid')
    fig = plt.figure(figsize=(20,30))
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.5)

    rows = math.ceil(float(train.shape[1]) / 3)

    j = 0

    for i, column in enumerate(train.columns):

        if train.dtypes[column] != np.object:

            ax = fig.add_subplot(rows, 3, j + 1)
            ax.set_title(column)

            sns.distplot(train[column], hist=False, rug=True, label="train")
            sns.distplot(test[column], hist=False, rug=True, label="test")

            plt.legend()

            plt.xticks(rotation=25)

            j = j+1

def canonicalize_dataset(df):

        # Replace '?' with null values and keep rows where Viability is not null
        df = df.replace('?', np.nan)
        df = df[df['Viability'].notna()]

        # Replace floating-point comma with dot and make sure numerical columns have numeric data type

        if(df["core_size_nm"].dtype == np.object):
                df["core_size_nm"] = df["core_size_nm"].str.replace(',','.')
        df["core_size_nm"] = pd.to_numeric(df["core_size_nm"])
        df["core_size_nm"] = df["core_size_nm"].astype(float)

        if(df["hydro_size_nm"].dtype == np.object):
                df["hydro_size_nm"] = df["hydro_size_nm"].str.replace(',','.')
        df["hydro_size_nm"] = pd.to_numeric(df["hydro_size_nm"])
        df["hydro_size_nm"] = df["hydro_size_nm"].astype(float)

        if(df["Surf_charge_mV"].dtype == np.object):
                df["Surf_charge_mV"] = df["Surf_charge_mV"].str.replace(',','.')
        df["Surf_charge_mV"] = pd.to_numeric(df["Surf_charge_mV"])
        df["Surf_charge_mV"] = df["Surf_charge_mV"].astype(float)

        if(df["Surface_area_m2_g"].dtype == np.object):
                df["Surface_area_m2_g"] = df["Surface_area_m2_g"].str.replace(',','.')
        df["Surface_area_m2_g"] = pd.to_numeric(df["Surface_area_m2_g"])
        df["Surface_area_m2_g"] = df["Surface_area_m2_g"].astype(float)

        if(df["Dose_microg_mL"].dtype == np.object):
                df["Dose_microg_mL"] = df["Dose_microg_mL"].str.replace(',','.')
        df["Dose_microg_mL"] = pd.to_numeric(df["Dose_microg_mL"])
        df["Dose_microg_mL"] = df["Dose_microg_mL"].astype(float)

        if(df["Viability"].dtype == np.object):
                df["Viability"] = df["Viability"].str.replace(',','.')
        df["Viability"] = pd.to_numeric(df["Viability"])
        df["Viability"] = df["Viability"].astype(float)

        if(df["Duration_h"].dtype == np.object):
                df["Duration_h"] = df["Duration_h"].str.replace(',','.')
        df["Duration_h"] = pd.to_numeric(df["Duration_h"])
        df["Duration_h"] = df["Duration_h"].astype(float)

        print("Does numeric columns have float64 pandas type? \n")
        print("Duration_h: " + str(pd.api.types.is_numeric_dtype(df['Duration_h'])))
        print("core_size_nm: " + str(pd.api.types.is_numeric_dtype(df['core_size_nm'])))
        print("hydro_size_nm: " + str(pd.api.types.is_numeric_dtype(df['hydro_size_nm'])))
        print("Surf_charge_mV: " + str(pd.api.types.is_numeric_dtype(df['Surf_charge_mV'])))
        print("Surface_area_m2_g: " + str(pd.api.types.is_numeric_dtype(df['Surface_area_m2_g'])))
        print("Dose_microg_mL: " + str(pd.api.types.is_numeric_dtype(df['Dose_microg_mL'])))
        print("Duration_h: " + str(pd.api.types.is_numeric_dtype(df['Duration_h'])))
        print("Viability: " + str(pd.api.types.is_numeric_dtype(df['Viability'])))

        df = df.round(decimals = 2)

        df['Assay'] = df['Assay'].str.strip()
        df['NP_type'] = df['NP_type'].str.strip()
        df['shape'] = df['shape'].str.strip()
        df['Cell_name'] = df['Cell_name'].str.strip()
        df['Cell_species'] = df['Cell_species'].str.strip()
        df['cell_Organ'] = df['cell_Organ'].str.strip()
        df['Cell_morphology'] = df['Cell_morphology'].str.strip()
        df['Cell_age'] = df['Cell_age'].str.strip()
        df['cell_type'] = df['cell_type'].str.strip()
        df['sex'] = df['sex'].str.strip()
        df['Assay'] = df['Assay'].str.strip()

        df = df.drop_duplicates()
        df = df.reset_index(drop=True)


        df["nanomaterial_group"] = df["NP_type"]

        metal_oxides = ["SiO2", "MgO", "TiO2", "ZnO", "Bi2O3", "CuO", "Cu2O", "Fe3O4", "IronOxide", "MnO", "ZrO2", "Co3O4", "CoO",
                            "Mn2O3", "Ni2O3", "Al2O3", "Fe2O3", "In2O3", "La2O3", "NiO", "Sb2O3", "SnO2", "Y2O3", "CeO2", "CdO", "Dy2O3",
                            "Er2O3", "Eu2O3", "Gd2O3", "HfO2", "MnO2", "Nd2O3", "Sm2O3", "Yb2O3", "Cr2O3"]
        carbon = ["Graphite", "Diamond", "C60", "C70", "Carbon"]
        nanotubes = ["Nanotubes", "SWCNT", "MWCNT"]
        quantum_dots = ['CdSe', 'CdTe', 'CdSeTe', 'CdZnS', 'CdS', 'CdTeS', 'CdHgTe', 'CdSeS', 'CdGeS', 'CdGdTe', 'CdZnSeS', 'QD', 'QDs']

        combined_groups = list(metal_oxides + carbon + nanotubes + quantum_dots)

        df.loc[df["NP_type"].isin(metal_oxides), "nanomaterial_group"] = "meta_oxide"
        df.loc[df["NP_type"].isin(carbon), "nanomaterial_group"] = "carbon"
        df.loc[df["NP_type"].isin(nanotubes), "nanomaterial_group"] = "nanotubes"
        df.loc[df["NP_type"].isin(quantum_dots), "nanomaterial_group"] = "quantum_dots"
        df.loc[~df["NP_type"].isin(combined_groups), "nanomaterial_group"] = "other"

        df.insert(len(df.columns)-2, 'nanomaterial_group', df.pop('nanomaterial_group'))

        #df = df.dropna(subset=['hydro_size_nm', 'Surf_charge_mV', 'Surface_area_m2_g', 'shape'], thresh=2)

        print("\nFinal column types: \n")
        print(df.dtypes)

        print("\nNP types that fall into the 'other' group:")
        print(df['NP_type'][~df['NP_type'].isin(combined_groups)].unique())

        return df

def convert_to_classification_dataset(df):
    df["viability_class"] = df["Viability"]
    df.loc[df["Viability"] < 50.0, "viability_class"] = "Toxic"
    df.loc[df["Viability"] >= 50.0, "viability_class"] = "NonToxic"
    df = df.drop('Viability', axis=1)

    return df

def quantile_discretize(df, y):

    df[y+'_discrete'] = pd.qcut(df[y], q=5)

    return df

def round_float(s):

    import re
    m = re.match("(\d+\.\d+)",s.__str__())
    try:
        r = round(float(m.groups(0)[0]),2)
    except:
        r = s
    return r