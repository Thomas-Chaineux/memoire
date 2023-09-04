import xml.etree.ElementTree as ET
import pandas as pd

cols = ['Class','rico:identifier', 'rico:hasRecordSetType', 'dcterms:title', 'dcterms:description','rico:dateInterv', 'rico:dateRaw', 'rico:hasCreatorRef', \
        'rico:hasCreatorNotRef', 'rico:hasReceiverRef', "rico:hasReceiverNotRef", "rico:hasPublisher", 'rico:isOrWasIncludedIn', \
        "rico:hasOrHadPhysicalLocation", "crm:P44_has_condition"]
rows = []

xmlfile = '/home/thomas/Bureau/Stage/Inventaires et référentiels/Inventaires_LL/Conversion Excel-EAD/ARCHIVES_VARAGNES_inventaire_complet_EAD_juillet_2023.xml'
xmlparse = ET.parse(xmlfile)
root = xmlparse.getroot()

nom_fichier_sortie = 'IMPORT_Archives_CSV.csv'

set_archives_class = "rico:RecordSet"
item_archives_class = "rico:Record"

for c_element in root.findall(".//c"):

#Determiner l'élément parent
    parent_c_element = None
    for element in root.iter():
        if c_element in element:
            parent_c_element = element
            break


    c_level_descr = c_element.attrib.get("level")
    if c_element.attrib.get("otherlevel"):
        c_level_otherlevel = c_element.attrib.get("otherlevel")

        #Definition de la classe de l'item et du type de 
    if c_level_descr == "subfonds":
        archives_class = set_archives_class
        record_set_type = "Sous-fonds d'archives"
    elif c_level_descr == "series":
        archives_class = set_archives_class
        record_set_type = "Série d'archives"
    elif c_level_descr == "subseries":
        archives_class = set_archives_class
        record_set_type = "Sous-série d'archives"
    elif c_level_descr == "file":
        archives_class = set_archives_class
        record_set_type = "Dossier d'archives"
    elif c_level_descr == "otherlevel" and c_level_otherlevel == "subfile":
        archives_class = set_archives_class
        record_set_type = "Sous-dossier d'archives"
    elif c_level_descr == "otherlevel" and c_level_otherlevel == "subsubfile":
        archives_class = set_archives_class
        record_set_type = "Sous-sous-dossier d'archives"
    elif c_level_descr == "item":
        archives_class = item_archives_class
        record_set_type = ""


    did_element = c_element.find("./did")
    unitid_element = did_element.find("./unitid")

    unitdate_element = did_element.find("./unitdate")
    unitdate_attrib_normal = unitdate_element.attrib.get('normal')
    if "/" in unitdate_attrib_normal and unitdate_attrib_normal != "/":#selon que la date soit un intervalle ou non, elle va dans une colonne différente
        unitdate_intervalle = unitdate_attrib_normal
        unitdate_raw = ""
    else: 
        unitdate_intervalle=""
        unitdate_raw = unitdate_attrib_normal

    unittitle_element = did_element.find("./unittitle")
    unittitle_title_element = unittitle_element.find("./title")



    #TRAITEMENT DE ORIGINATION, avec distinction selon que l'auteur soit référencé ou non
    origination_elements = did_element.findall("./origination")  # renvoie une liste (liste vide s'il n'y a pas d'éléments origination)
    if origination_elements:  # s'il y a du contenu dans origination_elements
        origination_notref = []
        origination_ref = []
        for auteur in origination_elements:
            persname_element = auteur.find("./persname")
            if persname_element is not None:  # s'il y a un élément persname dans origination
                origination_ref.append(persname_element.attrib.get("authfilenumber"))
            else:
                origination_notref.append(auteur.text)
        origination_notref = ';'.join(origination_notref)  # convertit la liste en une chaîne de caractères séparée par des ';'
        origination_ref = ';'.join(origination_ref)  # convertit la liste en une chaîne de caractères séparée par des ';'
    else:
        origination_notref = ""
        origination_ref = ""



    #TRAITEMENT DE MATERIALSPEC, avec distinction selon que ce soit un imprimeur ou un destinataire, puis selon si le destinataire est référencé ou non
    materialspec_elements = did_element.findall("./materialspec")
    if materialspec_elements:
        destinataire_ref = []
        destinataire_not_ref = []
        for materialspec in materialspec_elements:
            if materialspec.attrib.get("type") == 'Imprimeur':
                imprimeur = materialspec.text
            elif materialspec.attrib.get("type") == "Destinataire":
                imprimeur = ""
                ref_element = materialspec.find("./ref")
                if ref_element is not None:
                    destinataire_ref.append(ref_element.attrib.get("href"))
                else:
                    destinataire_not_ref.append(materialspec.text)
        destinataire_ref = ";".join(destinataire_ref)
        destinataire_not_ref = ";".join(destinataire_not_ref)
    else:
        imprimeur = ""
        destinataire_ref = ""
        destinataire_not_ref = ""


    
    #DETERMINER LE CONTENANT DE L'ELEMENT C
    if parent_c_element is not None: 
        parent_c_element_did = parent_c_element.find("./did/unitid")        
        contenu_dans = parent_c_element_did.text if parent_c_element_did is not None else ""
    else:
        contenu_dans = ""


    

    

    

    physloc_element = did_element.find("./physloc")
    if physloc_element is not None: 
        physloc = physloc_element.text
    else:
        physloc = ""

    
    physdesc_element = did_element.find("./physdesc")
    if physdesc_element is not None: 
        physdesc = physdesc_element.text
    else: 
        physdesc = ""

   
    rows.append({"Class": archives_class,
                 "rico:identifier": unitid_element.text if unitid_element is not None else "",
                 'rico:hasRecordSetType': record_set_type,
                 'dcterms:title': unittitle_title_element.text if unittitle_title_element is not None else "",
                 'dcterms:description': unittitle_element.text if unittitle_element is not None else "",
                 'rico:dateInterv': unitdate_intervalle,
                 'rico:dateRaw': unitdate_raw, 
                 'rico:hasCreatorRef': origination_ref,
                 'rico:hasCreatorNotRef': origination_notref,
                 'rico:hasReceiverRef':destinataire_ref,
                 "rico:hasReceiverNotRef": destinataire_not_ref,
                 "rico:hasPublisher": imprimeur,
                 'rico:isOrWasIncludedIn':contenu_dans,
                 "rico:hasOrHadPhysicalLocation": physloc,
                 "crm:P44_has_condition":physdesc})

df = pd.DataFrame(rows, columns=cols)
df.to_csv(nom_fichier_sortie, index=False)
