import os
import sys
import csv

# folder containing files to be converted
# architecture of subfolders is as follows
# folder
#   election
#       src (sources files)
#       xls (resulting excel sheets)
#       csv (resulting csv)
folder_input = sys.argv[1]

# dictionary of election types
elec_types = {
    "2" : "présidentielle",
    "3" : "législative",
    "5" : "municipale",
    "9" : "européenne",
}

# function to complete election year
def whatyearisthis(truncatedyear):
    truncatedyear_int = int(truncatedyear)
    if truncatedyear_int < 28:
        return "20" + truncatedyear
    else :
        return "19" + truncatedyear

# parser for .NOM files
def parsenomnom(nomfile_path):
    nom_nom = open(nomfile_path, 'r', encoding='CP437').readlines()
    nom_nom = [nom.strip() for nom in nom_nom]
    return nom_nom

# generic headers for output files
headers = ["geo", "type", "year", "turn", "inscrits", "votants", "exprimés"]

# for each election folder define its path
for election in os.listdir(folder_input):
    election_src_path = os.path.join(folder_input, election, "src")

    # for each source file in the election folder, define path
    for src_file in os.listdir(election_src_path):
        src_file_path = os.path.join(election_src_path, src_file)

        # if the file is a .NOM file, build a dictionary of names out of it
        if src_file.endswith('.NOM'):
            src_file = open(src_file_path, 'r', encoding='CP437').readlines()
            candidates = {}
            for i in range(len(src_file)):
                candidates[i+1] = src_file[i].strip()

        # if the file is a .CIR file, extract its content
        elif src_file.endswith('.CIR'):
            src_file = open(src_file_path, 'r', encoding='CP437')
            for line in src_file:
                # print(line)

                dep_num = line[:2]
                circo_num = line[2:4]
                elec_type = line[4]
                elec_year = line[5:7]
                elec_turn = line[7]

                elec_info = line[8:32]
                [inscrits, votants, exprimes] = [elec_info[i:i + 8] for i in range(0, len(elec_info), 8)]

                results = line[32:]
                results = [results[i:i + 10].strip() for i in range(0, len(results)-1, 10)]
                results = [x.split()[1] for x in results]
                # print(results)

        elif src_file.endswith('.DEP'):
            src_file = open(src_file_path, 'r', encoding='CP437')
            out_path = src_file_path.replace('src', 'csv').replace('.DEP', '.csv')
            out_file = csv.writer(open(out_path, 'w'))
            out_headers = headers + parsenomnom(src_file_path.replace('.DEP', '.NOM'))
            out_file.writerow(out_headers)
            for line in src_file:
                # print(line)
                dep_num = line[:2]
                elec_type = line[2]
                elec_year = line[3:5]
                elec_turn = line[5]

                elec_info = line[6:30]
                [inscrits, votants, exprimes] = [int(elec_info[i:i + 8].strip()) for i in range(0, len(elec_info), 8)]

                results = line[30:]
                results = [results[i:i + 10].strip() for i in range(0, len(results)-1, 10)]
                results = [x.split()[1] for x in results]

                out_line = [dep_num, elec_types[elec_type], whatyearisthis(elec_year), elec_turn, inscrits, votants, exprimes]
                out_line.extend(results)
                out_file.writerow(out_line)


        # if the file is a .VIL file, extract its content
