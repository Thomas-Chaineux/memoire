# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from datetime import datetime
import re


import xml.etree.ElementTree as ET

import logging


#####################
##### Ce fichier prend l'inventaire Excel, consertit ses données selon un XML EAD, et insère le résultat dans 
##### un fichier d'entrée qui contient une introduction (FICHIER_ENTREE_intro_inventaire_varagnes_ead.xml).
##### Le résultat est un nouveau fichier XML EAD directement valide (ARCHIVES_VARAGNES_inventaire_complet_EAD_juillet_2023.xml)
#####################



logger = logging.getLogger(__name__)
#logger.setLevel('WARNING')
logger.setLevel('INFO')
#logger.setLevel('DEBUG')

root_dir = '/home/thomas/Bureau/Stage/Inventaires et référentiels/Inventaires_LL/Conversion Excel-EAD/'

dtype_xls = {
    'ID OS auteur': str
    }

xls_df = pd.read_excel(root_dir + 'DOC_TRAVAIL_inventaire_complet_nettoye_et_annote_FINAL_juillet_2023.xlsx', dtype=dtype_xls)# LECTURE DU EXCEL

# Dictionnaire subfonds
group_cb = xls_df[['Grande catégorie','Cote de la boîte']].groupby(by=['Grande catégorie']).agg(['first','last'])
group_cb['cote-groupée']=group_cb['Cote de la boîte']['first'] + '-' + group_cb['Cote de la boîte']['last']
group_deb = xls_df[['Grande catégorie','Année de début']].groupby(by=['Grande catégorie']).agg(['min']).fillna(0)
group_fin = xls_df[['Grande catégorie','Année de fin']].groupby(by=['Grande catégorie']).agg(['max']).fillna(0)
group_df = pd.concat([group_cb,group_deb,group_fin], axis=1)
group_df['dates extremes'] = group_df['Année de début']['min'].astype(int).astype(str).replace('0','')\
    + '-' \
    + group_df['Année de fin']['max'].astype(int).astype(str).replace('0','')
group_df['dates normales'] = group_df['Année de début']['min'].astype(int).astype(str).replace('0','')\
    + '/' \
    + group_df['Année de fin']['max'].astype(int).astype(str).replace('0','')


# Dictionnaire series
group2_cb = xls_df[['Grande catégorie', "Nature de l'archive", 'Cote de la boîte']].groupby(by=['Grande catégorie', "Nature de l'archive"]).agg(['first', 'last'])
group2_cb['cote-groupée'] = group2_cb['Cote de la boîte']['first'] + '-' + group2_cb['Cote de la boîte']['last']
group2_deb = xls_df[['Grande catégorie',"Nature de l'archive",'Année de début']].groupby(by=['Grande catégorie',"Nature de l'archive"]).agg(['min']).fillna(0)
group2_fin = xls_df[['Grande catégorie',"Nature de l'archive",'Année de fin']].groupby(by=['Grande catégorie',"Nature de l'archive"]).agg(['max']).fillna(0)
group2_df = pd.concat([group2_cb,group2_deb,group2_fin], axis='columns')
group2_df['dates extremes'] = group2_df['Année de début']['min'].astype(int).astype(str).replace('0','') \
    + '-' \
    + group2_df['Année de fin']['max'].astype(int).astype(str).replace('0','')

group2_df['dates normales'] = group2_df['Année de début']['min'].astype(int).astype(str).replace('0','') \
    + '/' \
    + group2_df['Année de fin']['max'].astype(int).astype(str).replace('0','')

# Dictionnaire sub-series
group3_deb = xls_df[['Grande catégorie',"Nature de l'archive",'Cote de la boîte','Année de début']].groupby(by=['Grande catégorie',"Nature de l'archive",'Cote de la boîte']).agg(['min']).fillna(0)
group3_fin = xls_df[['Grande catégorie',"Nature de l'archive",'Cote de la boîte','Année de fin']].groupby(by=['Grande catégorie',"Nature de l'archive",'Cote de la boîte']).agg(['max']).fillna(0)
group3_df = pd.concat([group3_deb,group3_fin], axis='columns')
group3_df['dates extremes'] = group3_df['Année de début']['min'].astype(int).astype(str).replace('0','') \
    + '-' \
    + group3_df['Année de fin']['max'].astype(int).astype(str).replace('0','')
group3_df['dates normales'] = group3_df['Année de début']['min'].astype(int).astype(str).replace('0','')\
    + '/' \
    + group3_df['Année de fin']['max'].astype(int).astype(str).replace('0','')




xls_idx_df = xls_df.set_index(['Grande catégorie',"Nature de l'archive", 
                           'Cote de la boîte',])

#############
##
############
                
def tostr(num):
    x = ''
    try:
        x = str(int(num))
    except ValueError as e:
        print(num)
        print(e)

    if len(x) == 1:
        x = '0' + x
    return x
           
def date_from_piece(piece_df):
    unitdate_text = ''
    unitdate_norm = ''
    start_txt = ''
    start_norm = ''
    start_dt = None
    
    end_txt = ''
    end_norm = ''
    end_dt = None
    
    piece_df = piece_df.fillna('')
    
    year_start = piece_df['Année de début']
    month_num_start = piece_df['Mois de début (chiffres)']
    month_name_start = piece_df['Mois de début (lettres)']
    day_start = piece_df['Jour de début']
    
    year_end = piece_df['Année de fin']
    month_num_end = piece_df['Mois de fin (chiffres)']
    month_name_end = piece_df['Mois de fin (lettres)']
    day_end = piece_df['Jour de fin']
    
    # Date start
    if not year_start == '': #si la colonne Année de début n'est pas vide
        year_start = tostr(year_start)
        start_txt = year_start
        start_norm = year_start
        start_dt = pd.to_datetime(start_norm,format='%Y')#L'assemblage en format date permet de comparer les valeurs concaténées de début et de fin
        
        if not month_num_start == '': #Si le mois n'est pas vide, on complète 
            month_num_start = tostr(month_num_start)
            start_txt = month_name_start + ' ' + year_start
            start_norm = year_start + '-' + month_num_start
            start_dt = pd.to_datetime(start_norm,format='%Y-%M')
            
            if not day_start == '':#si le jour n'est pas vide, on complète
                day_start = tostr(day_start)
                start_txt = day_start + ' ' + month_name_start + ' ' + year_start
                start_norm = year_start + '-' + month_num_start + '-' + day_start
                start_dt = pd.to_datetime(start_norm,format='%Y-%M-%d')
    # Date end
    if not year_end == '': 
        year_end = tostr(year_end)
        end_txt = year_end
        end_norm = year_end
        end_dt = pd.to_datetime(end_norm,format='%Y')
        
        if not month_num_end == '': #le mois existe 
            month_num_end = tostr(month_num_end)
            end_txt = month_name_end + ' ' + year_end
            end_norm = year_end + '-' + month_num_end
            end_dt = pd.to_datetime(end_norm,format='%Y-%M')
            
            if not day_end == '':
                day_end = tostr(day_end)
                end_txt = day_end + ' ' + month_name_end + ' ' + year_end
                end_norm = year_end + '-' + month_num_end + '-' + day_end
                end_dt = pd.to_datetime(end_norm,format='%Y-%M-%d')#L'assemblage en format date permet de comparer les valeurs concaténées de début et de fin

    
    if year_start == '' and year_end == '':#si les champs dates sont vides, on met le texte en s.d.
        unitdate_text='s.d.'
    else:
        if not year_end == '':#si la colonne Année de fin n'est pas vide
            if end_dt == start_dt:#si les dates montées et comparées sont égales
                unitdate_text = start_txt#seule la valeur de début est prise pour le texte
                unitdate_norm = start_norm#seule la valeur de début est prise pour la norme ISO
            elif end_dt > start_dt:#si la date de fin est plus grande
                unitdate_text = start_txt + '-' + end_txt#on concatène les valeurs pour le textes
                unitdate_norm = start_norm + '/' + end_norm#on concatène les valeurs pour la norme ISO
        elif not year_start == '':
            #start date exists but not end date
            unitdate_text = start_txt
            unitdate_norm = start_norm
        else:
            raise ValueError('scenario of dates not implemented')
            
    logger.debug(' '*21+ 
                 '<unitdate_text>' + unitdate_text +
                 '<unitdate_norm>' + unitdate_norm )
    return (unitdate_text, unitdate_norm)
   
    
def write_auteur(did, piece_df):
    
    piece_df = piece_df.fillna('')
    
    auteur_cell = piece_df['Auteur']#lecture colonne Auteur (Marc Seguin)
    auteur_ref_cell = piece_df['Auteur référencé']#Lecture colonne Auteur référence (REFPERS0002)
    
    
    if not auteur_cell == '':#SI Cellule Auteur n'est pas vide
        auteur_list = auteur_cell.split(';')#Split de la cellule Auteur (texte) selon ";"
        for idx, auteur in enumerate(auteur_list):#pour chaque ID et auteur distincts dans l'énumération post-split
            logger.debug(' '*21+'<auteur>'+auteur)
            origination = ET.SubElement(did,'origination')#l'élément <origination> est créé sous <did>            

            # <persname authfilenumber="item/81">Marc Seguin</persname>
            #id_os_cell = piece_df['ID OS auteur']#Lecture colonne ID OS auteur
            if not auteur_ref_cell == '':#si cellule ID OS auteur n'est pas vide
                auteur_ref_cell_list = str(auteur_ref_cell).split(';')#Conversion en string et split selon ";" des ID OS
                if len(auteur_ref_cell_list) == len(auteur_list):#Si la longueur des id d'auteurs est égale à la longueur des auteurs écrits
                    logger.debug(' '*21+'<id_os>'+auteur_ref_cell_list[idx])
                    persname = ET.SubElement(origination,'persname')#création d'un élément <persname> sous <origination>
                    persname.text = auteur#le texte de <persname> est égal à l'auteur écrit (variable for)
                    persname.set('authfilenumber ', auteur_ref_cell_list[idx] ) 
                    
                else:   #erreur si la longueur des id d'auteurs n'est pas égale à la longueur des auteurs écrits                 
                    logger.warning('WARNING ! len(auteur_ref_cell_list) != len(auteur_list)')
                    logger.warning(auteur_list)
                    logger.warning(auteur_ref_cell_list)
            else:#soit si auteur ID est vide
                origination.text = auteur#le contenu de Auteur écrit
                logger.debug(' '*21+'<auteur>'+auteur)

        
def write_destin(did, piece_df):
    piece_df = piece_df.fillna('')
    destin_cell = piece_df['Destinataire /Imprimeur']#Lecture colonne Destinataire /Imprimeur (Texte)
    destin_ref_cell = piece_df['Destinataire référencé']#Lecture colonne Destinataire référencé (REFPERS00XX)
    destin_id_cell = str(piece_df['ID OS destin.'])#Lecture colonne IS OS destin (ref Omeka)
    
    if destin_cell:
        destin_list = destin_cell.split(';')
        for idx, destin in enumerate(destin_list):
            logger.debug(' '*21+'<destinataire>'+destin)
            materialspec = ET.SubElement(did,'materialspec')
            materialspec.set('type','Destinataire')

            if destin_ref_cell:
                destin_ref_cell_list = str(destin_ref_cell).split(';')
                if len(destin_ref_cell_list) == len(destin_list):
                    logger.debug(' '*21+'<id_number'+destin_ref_cell_list[idx])
                    ref = ET.SubElement(materialspec, 'ref')
                    ref.text = destin
                    ref.set('href', destin_ref_cell_list[idx])
                else:
                    logger.warning('WARNING! len(destin_ref_cell_list != len (destin_list)')
                    logger.warning(destin_list)
                    logger.warning(destin_ref_cell_list)
            else:
                materialspec.text = destin
                logger.debug(' '*21+'<destinataire>'+destin)



def write_imprimeur(did, piece_df):
    piece_df=piece_df.fillna('')
    imprimeur_cell = piece_df['Imprimeur']

    if imprimeur_cell:
        materialspec = ET.SubElement(did,'materialspec')
        materialspec.text = imprimeur_cell
        materialspec.set('type','Imprimeur')


def write_physdesc(did, piece_df):
    piece_df = piece_df.fillna('')
    physdesc_cell = piece_df['Observation sur l\'état matériel']
    if physdesc_cell != '':
        physdesc = ET.SubElement(did,'physdesc')
        physdesc.text = physdesc_cell
        

def write_items(parent_xml, parent_df): 
    np = parent_df.iloc[0]['numéro de la pièce']
    if np == np: # il y a au moins une piece  
        for piece, piece_df in parent_df.groupby(by='numéro de la pièce'):               
            logger.info('                   <item>'+piece)
            
            if type(piece_df.iloc[0] ) == str:
                piece_0_df = piece_df
            else: 
                piece_0_df = piece_df.iloc[0] 

            description = piece_0_df.fillna('')['Description'].strip()
            titrepiece = piece_0_df.fillna('')['Titre de la pièce'].strip()
            
            item = ET.SubElement(parent_xml,'c')
            item.set('level', 'item')
            did = ET.SubElement(item,'did')
            unitid=ET.SubElement(did,'unitid')
            unitid.text = piece.strip()
            unittitle = ET.SubElement(did,'unittitle')
            unittitle.text = description
            if not titrepiece == '':
                title = ET.SubElement(unittitle,'title')
                title.text = titrepiece
            unitdate = ET.SubElement(did,'unitdate')
            (unitdate_text, unitdate_norm) = date_from_piece(piece_0_df)
            unitdate.text = unitdate_text
            unitdate.set('calendar', 'gregorian')
            unitdate.set('era', 'ce')
            unitdate.set('normal', unitdate_norm)
            
            write_auteur(did, piece_0_df)
            write_destin(did, piece_0_df)
            write_imprimeur(did, piece_0_df)
            write_physdesc(did, piece_0_df)
            

# build_xml(xls_idx_df)

#############
##
############


def build_xml(xls_idx_df):
        
    tree = ET.parse(root_dir+'FICHIER_ENTREE_intro_inventaire_varagnes_ead.xml')
    root = tree.getroot()
    
    dsc_element = root.find(".//dsc")    

    for gc, subf_df in xls_idx_df.groupby(level=0):#1ère boucle For pour les sous-fonds
        logger.info('<subfonds>'+gc)
        subf = ET.SubElement(dsc_element,'c')
        subf.set('level', 'subfonds')
        did = ET.SubElement(subf,'did')
        unitid=ET.SubElement(did,'unitid')
        unitid.set('type', 'cote-groupee')
        unitid.text = group_df.loc[gc,'cote-groupée'][0]
        unittitle = ET.SubElement(did,'unittitle')
        unittitle.text = gc
        unitdate = ET.SubElement(did,'unitdate')
        unitdate.set('calendar','gregorian')
        unitdate.set('era','ce')
        unitdate.set('normal', group_df.loc[gc,'dates normales'][0])
        unitdate.text = group_df.loc[gc,'dates extremes'][0]
        
        for na, serie_df in subf_df.groupby(level=1):#2e boucle For pour les séries
            logger.info('   <series>'+na)
            serie = ET.SubElement(subf,'c')
            serie.set('level', 'series')
            did = ET.SubElement(serie,'did')
            unitid=ET.SubElement(did,'unitid')
            unitid.set('type', 'cote-groupee')
            unitid.text = group2_df.loc[(gc,na),'cote-groupée']
            unittitle = ET.SubElement(did,'unittitle')
            unittitle.text = na
            unitdate = ET.SubElement(did,'unitdate')
            unitdate.set('calendar','gregorian')
            unitdate.set('era','ce')
            unitdate.set('normal', group2_df.loc[(gc,na),'dates normales'])
            unitdate.text = group2_df.loc[(gc,na),'dates extremes']
                
            for boite, boite_df in serie_df.groupby(level=2):#3e boucle For pour les boîtes (les sous-séries)
                logger.info('      <series>'+boite)
                subserie = ET.SubElement(serie,'c')
                subserie.set('level', 'subseries')
                did = ET.SubElement(subserie,'did')
                unitid=ET.SubElement(did,'unitid')
                unitid.text = boite
                unittitle = ET.SubElement(did,'unittitle')
                unittitle.text = boite_df['Nom de la boîte'][0]
                unitdate = ET.SubElement(did,'unitdate')
                unitdate.set('calendar','gregorian')
                unitdate.set('era','ce')
                unitdate.set('normal', group3_df.loc[(gc,na,boite),'dates normales'])
                unitdate.text = group3_df.loc[(gc,na,boite),'dates extremes']
                physloc=ET.SubElement(did,'physloc')
                physloc.text = boite_df['Localisation actuelle'][0]
        
                nd= boite_df.iloc[0]['Cote du dossier']        
    
                if not nd == nd: #si dossier n'existe pas
                    write_items(subserie,boite_df)
                else:#si dossier existe

                    
                    for dossier, dossier_df in boite_df.groupby(by='Cote du dossier'):#pour chaque dossier dans la sous-série, groupé par cote du dossier
                        logger.info('         <file>'+dossier)
                        
                        file = ET.SubElement(subserie,'c')#crée un sous élément <c> dans l'élément sous-série
                        file.set('level', 'file')# et lui donne l'attribut level="file"
                        did = ET.SubElement(file,'did')#et un sous élément <did>
                        unitid=ET.SubElement(did,'unitid')#ceée un sous-élément <unitid> à <did>
                        unitid.text = dossier#le contenu de <unitid> est égal à la valeur de dossier
                        unittitle = ET.SubElement(did,'unittitle')#ceée un sous-élément <unittitle> à <did>
                        unittitle.text = dossier_df['Nom du dossier'][0]
                        unitdate = ET.SubElement(did,'unitdate')#ceée un sous-élément <unitdate> à <did>
                        unitdate.set('calendar', 'gregorian')
                        unitdate.set('era', 'ce')

                        min_date_dossier = dossier_df['Année de début'].min()
                        max_date_dossier = dossier_df['Année de fin'].max()
                        
                        min_date_dossier_str = str(int(min_date_dossier)) if pd.notnull(min_date_dossier) else ""
                        max_date_dossier_str = str(int(max_date_dossier)) if pd.notnull(max_date_dossier) and min_date_dossier != max_date_dossier else ""
                        #max date, SI max date non nul ET différent de min date, SINON rien
                        

                        if min_date_dossier_str:
                            unitdate.text = min_date_dossier_str + ('-' + max_date_dossier_str if max_date_dossier_str else '')
                            unitdate_dossier_normal = min_date_dossier_str + ('/' + max_date_dossier_str if max_date_dossier_str else '')
                            unitdate.set('normal', unitdate_dossier_normal )                            
                        else :
                            unitdate.text="s.d."
                            unitdate.set('normal', '')
                                        
                    



                        nsd= dossier_df.iloc[0]['Numéro du sous-dossier']
                        
                        if not nsd == nsd: 
                            write_items(file, dossier_df)    
                        else: #if nsd exists
        
                            for sousdossier, sousdossier_df in dossier_df.groupby(by='Numéro du sous-dossier'):
                                logger.info('            <subfile>'+sousdossier)
                                subfile = ET.SubElement(file,'c')
                                subfile.set('level', 'otherlevel')
                                subfile.set('otherlevel', 'subfile')
                                did = ET.SubElement(subfile,'did')
                                unitid=ET.SubElement(did,'unitid')
                                unitid.text = sousdossier
                                unittitle = ET.SubElement(did,'unittitle')
                                unittitle.text = sousdossier_df['Nom du sous-dossier'][0]
                                unitdate = ET.SubElement(did,'unitdate')
                                unitdate.set('calendar', 'gregorian')
                                unitdate.set('era', 'ce')

                                min_date_sousdossier = sousdossier_df['Année de début'].min()
                                max_date_sousdossier = sousdossier_df['Année de fin'].max()
                                
                                min_date_sousdossier_str = str(int(min_date_sousdossier)) if pd.notnull(min_date_sousdossier) else ""
                                max_date_sousdossier_str = str(int(max_date_sousdossier)) if pd.notnull(max_date_sousdossier) and min_date_sousdossier != max_date_sousdossier else ""
                                        
                                if min_date_sousdossier_str:
                                    unitdate.text = min_date_sousdossier_str + ('-' + max_date_sousdossier_str if max_date_sousdossier_str else '')
                                    unitdate_sousdossier_normal = min_date_sousdossier_str + ('/' + max_date_sousdossier_str if max_date_sousdossier_str else '')
                                    unitdate.set('normal', unitdate_sousdossier_normal )                            
                                else :
                                    unitdate.text="s.d."
                                    unitdate.set('normal', '')
                                        

                                        
                                nssd= sousdossier_df.iloc[0]['Numéro du sous-sous-dossier']
                            
                                if not nssd == nssd: # if nssd exists
                                    write_items(subfile, sousdossier_df)    
                                else:
                                    for soussousdossier, soussousdossier_df in sousdossier_df.groupby(by='Numéro du sous-sous-dossier'):
                                        logger.info('               <subsubfile>'+soussousdossier)
                                        subsubfile = ET.SubElement(subfile,'c')
                                        subsubfile.set('level', 'otherlevel')
                                        subsubfile.set('otherlevel', 'subsubfile')
                                        did = ET.SubElement(subsubfile,'did')
                                        unitid=ET.SubElement(did,'unitid')
                                        unitid.text = soussousdossier
                                        unittitle = ET.SubElement(did,'unittitle')
                                        unittitle.text = soussousdossier_df['Nom du sous-sous-dossier'][0]
                                        unitdate = ET.SubElement(did,'unitdate')
                                        unitdate.set('calendar', 'gregorian')
                                        unitdate.set('era', 'ce')                                        

                                        min_date_soussousdossier = soussousdossier_df['Année de début'].min()
                                        max_date_soussousdossier = soussousdossier_df['Année de fin'].max()                                        
                                        min_date_soussousdossier_str = str(int(min_date_soussousdossier)) if pd.notnull(min_date_soussousdossier) else ""
                                        max_date_soussousdossier_str = str(int(max_date_soussousdossier)) if pd.notnull(max_date_soussousdossier) and min_date_soussousdossier != max_date_soussousdossier else ""
                                        if min_date_soussousdossier_str:
                                            unitdate.text = min_date_soussousdossier_str + ('-' + max_date_soussousdossier_str if max_date_soussousdossier_str else '')
                                            unitdate_soussousdossier_normal = min_date_soussousdossier_str + ('/' + max_date_soussousdossier_str if max_date_soussousdossier_str else '')
                                            unitdate.set('normal', unitdate_soussousdossier_normal )                            
                                        else :
                                            unitdate.text="s.d."
                                            unitdate.set('normal', '')                                        

                                        
                                        write_items(subsubfile, soussousdossier_df)    


    return tree



#############
##
############


tree = build_xml(xls_idx_df)

ET.indent(tree, space="    ")

tree.write(root_dir + 'ARCHIVES_VARAGNES_inventaire_complet_EAD_juillet_2023.xml')    


