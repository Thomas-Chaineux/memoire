import pandas as pd
import xml.etree.ElementTree as ET

#############
####Ce code prend le fichier ARCHIVES_VARAGNES_inventaire_complet_EAD_juillet_2023.xml (créé dans la transformation Excel => EAD)
####et y insère les ID de chaque item d'archives (contenu dans archives_fichier_general.csv) en tant qu'@attribut ID de chaque élément <c>
####afin de permettre de créer des liens vers la base lors de la transformation XSLT
#############


csv_file = "archives_fichier_general.csv"
df = pd.read_csv(csv_file)


xml_file = "ARCHIVES_VARAGNES_inventaire_complet_EAD_juillet_2023.xml"
tree = ET.parse(xml_file)
root = tree.getroot()


for c_elem in root.findall(".//c"):
    unitid_value = c_elem.find(".//unitid").text

    match_row = df[df["dcterms:identifier"] == unitid_value]

    if not match_row.empty:
        c_elem.set("id", str(match_row.iloc[0]["o:id"]))

output_xml_file = "data_modified.xml"
tree.write(output_xml_file)
