#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 19:17:14 2018

Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire 
et la pratique du dépassement d'honoraires ? Est-ce  dans les territoires où la densité 
est la plus forte que les médecins  pratiquent le moins les dépassement d'honoraires ? 
Est ce que la densité de certains médecins / praticiens est corrélé à la densité de
population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?

@author: margaux
"""

import pandas as pd

# Importation des données et mise en forme dans un DataFrame
filename = 'Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2016.xls'
sheets = ['Spécialistes', 'Généralistes et MEP', 'Dentistes et ODF', 'Sages-femmes', 'Auxiliaires médicaux']
file = pd.read_excel(filename, sheet_name = sheets, header = 0, skiprows = 0,
                     na_values = 'nc')
df = pd.DataFrame()
for elt in file:
    file[elt] = file[elt].rename(columns = {file[elt].columns[0] : 'Spécialité'})
    df = df.append(file[elt], ignore_index=True)
    
# Suppression des lignes de totaux
df = df.loc[~(df['Spécialité'].str.contains('TOTAL'))]

