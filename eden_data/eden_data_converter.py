import os
import sys
import csv

# TODO : ajouter l'intitulé des codes géographiques : DEP, VIL, CIR?

# path of folder containing files to be converted
folder_input = sys.argv[1]
# architecture of subfolders must be as follows
# folder
#   election
#     src (sources files)
#     xls (resulting excel sheets)
#     csv (resulting csv)

# dictionary of election types
elec_types = {
    "2" : "présidentielle",
    "3" : "législative",
    "5" : "municipale",
    "9" : "européenne",
}
# TODO : ajouter les codes manquants (régionales : 8)

# function to complete election year
def whatyearisthis(truncatedyear):
    truncatedyear_int = int(truncatedyear)
    if truncatedyear_int < 28:
        return "20" + truncatedyear
    else :
        return "19" + truncatedyear
# this function will have to be modified in 2028
# to prevent confusion between years 1928 and 2028

# parser for .NOM files, return an ordered array of political parties labels
def parsenomnom(nomfile_path):
    nom_nom = open(nomfile_path, 'r', encoding='CP437').readlines()
    nom_nom = [nom.strip() for nom in nom_nom]
    return nom_nom

# generic headers for output files
headers = ["geo", "type", "year", "turn", "inscrits", "votants", "exprimés"]

# for each election folder, define its path
for election in os.listdir(folder_input):
    election_src_path = os.path.join(folder_input, election, "src")
    print("Working on election " + election + " - (path : " + election_src_path + ")")

    # for each source file in the election folder, define path
    for src_file in os.listdir(election_src_path):
        src_file_path = os.path.join(election_src_path, src_file)

        # if the file is a .CIR file, extract its content
        if src_file.endswith('.CIR'):
            src_file = open(src_file_path, 'r', encoding='CP437')
            print("\tParsing .CIR file - (path : " + src_file_path + ")")

            # set output path, open output file stream, write output headers
            out_path = src_file_path.replace('src', 'csv') + ".csv"
            out_file = csv.writer(open(out_path, 'w'))
            out_headers = headers + parsenomnom(src_file_path.replace('.CIR', '.NOM'))
            out_file.writerow(out_headers)

            for line in src_file:
                # get infos from fixed-width .CIR csv
                dep_num = line[:2]
                circo_num = line[2:4]
                # TODO : check how to build circonum
                circo_num = (dep_num + circo_num).strip().zfill(4)
                elec_type = line[4]
                elec_year = line[5:7]
                elec_turn = line[7]
                elec_info = line[8:32]
                [inscrits, votants, exprimes] = [elec_info[i:i + 8] for i in range(0, len(elec_info), 8)]
                results = line[32:]
                results = [results[i:i + 10].strip() for i in range(0, len(results)-1, 10)]
                results = [x.split()[1] for x in results]
                # print(results)

                # create output csv line from the infos extracted, write it to output file stream
                out_line = [circo_num, elec_types[elec_type], whatyearisthis(elec_year), elec_turn, inscrits, votants, exprimes]
                # print(out_line)
                out_line.extend(results)
                out_file.writerow(out_line)

        # if the file is a .DEP file, extract its content
        elif src_file.endswith('.DEP'):
            src_file = open(src_file_path, 'r', encoding='CP437')
            print("\tParsing .DEP file - (path : " + src_file_path + ")")

            # set output path, open output file stream, write output headers
            out_path = src_file_path.replace('src', 'csv') + ".csv"
            out_file = csv.writer(open(out_path, 'w'))
            out_headers = headers + parsenomnom(src_file_path.replace('.DEP', '.NOM'))
            out_file.writerow(out_headers)

            for line in src_file:
                # print(line)
                # get infos from fixed-width .DEP csv
                dep_num = (line[:2]).strip().zfill(2)
                elec_type = line[2]
                elec_year = line[3:5]
                elec_turn = line[5]
                elec_info = line[6:30]
                [inscrits, votants, exprimes] = [int(elec_info[i:i + 8].strip()) for i in range(0, len(elec_info), 8)]
                results = line[30:]
                results = [results[i:i + 10].strip() for i in range(0, len(results)-1, 10)]
                results = [x.split()[1] for x in results]

                # create output csv line from the infos extracted, write it to output file stream
                out_line = [dep_num, elec_types[elec_type], whatyearisthis(elec_year), elec_turn, inscrits, votants, exprimes]
                # print(out_line)
                out_line.extend(results)
                out_file.writerow(out_line)

        # if the file is a .VIL file, extract its content
        elif src_file.endswith('.VIL'):
            src_file = open(src_file_path, 'r', encoding='CP437')
            print("\tParsing .VIL file - (path : " + src_file_path + ")")

            # set output path, open output file stream, write output headers
            out_path = src_file_path.replace('src', 'csv') + ".csv"
            out_file = csv.writer(open(out_path, 'w'))
            out_headers = headers + parsenomnom(src_file_path.replace('.VIL', '.NOM'))
            out_file.writerow(out_headers)

            for line in src_file:
                # print(line)
                # get infos from fixed-width .DEP csv
                dep_num = line[:2]
                vil_num = line[2:5]
                # TODO : check how to build vilnum
                vil_num = (dep_num + vil_num).strip().zfill(5)
                elec_type = line[5]
                elec_year = line[6:8]
                elec_turn = line[8]
                elec_info = line[9:33]
                [inscrits, votants, exprimes] = [int(elec_info[i:i + 8].strip()) for i in range(0, len(elec_info), 8)]
                results = line[33:]
                results = [results[i:i + 10].strip() for i in range(0, len(results)-1, 10)]
                results = [x.split()[1] for x in results]

                # create output csv line from the infos extracted, write it to output file stream
                out_line = [vil_num, elec_types[elec_type], whatyearisthis(elec_year), elec_turn, inscrits, votants, exprimes]
                # print(out_line)
                out_line.extend(results)
                out_file.writerow(out_line)
    print("\n")
