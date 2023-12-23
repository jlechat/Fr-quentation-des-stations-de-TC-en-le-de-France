import pandas as pd
from donnees_IDFM import donnees_validation_23
from pre_proces_Insee_IDFM import data_INSEE_stations

def df_validations():
    data=donnees_validation_23()
    data.loc[data['LIBELLE_ARRET'].isin(['CHATELET', 'LES HALLES']), 'lda'] = 474151
    data = data[data['LIBELLE_ARRET'] != 'MIRABEAU']
    aggregated_data = data.groupby(['JOUR', 'lda', 'CATEGORIE_TITRE'])['NB_VALD'].sum().reset_index()
    return aggregated_data


def df_stations():
    stations_RER=data_INSEE_stations()
    # Grouper les données par 'id_ref_ZdC' et appliquer une fonction personnalisée pour concaténer 'res_com'
    def concatenate_res_com(group):
        # Concaténer toutes les 'res_com' avec un séparateur, par exemple une virgule ou un espace
        return ', '.join(group['res_com'])
    
    # Appliquer la fonction personnalisée pour chaque groupe
    aggregated_stations = stations_RER.groupby('id_ref_ZdC').apply(concatenate_res_com).reset_index(name='res_com')
    unique_stations = stations_RER.drop_duplicates(subset='id_ref_ZdC').drop(columns=['res_com'])
    final_stations = unique_stations.merge(aggregated_stations, on='id_ref_ZdC')
    return final_stations