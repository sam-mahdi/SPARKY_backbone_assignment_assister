import re

"""Simply change the below lines to the names of your file"""
HNCA='G_ML_HNCA.list'
HNCACB='G_ML_HNCACB.list'
NHSQC='G_ML_Nhsqc.list'
"""These are tolerances that determine the range of peak variations accepted"""
carbon_tolerance=0.2
nitrogen_tolerance=0.1
hydrogen_tolerance=0.05

"""save files"""
i_table='i_table.txt'
i_minus_1_table='i-1_table.txt'
overlapping_peaks_table='overlapping_peaks_table.txt'
match_table='matches_table.txt'


def fun(hnca_list,hncacb_list,nhsqc_values,file,nhsqc_nitrogen,nhsqc_hydrogen):
    i_minus_1=[[],[],[],[]]
    carbon_list=[[],[],[],[]]
    counter=-1
    for i in range(2):
        alpha_carbon=float((hnca_list[i].split()[2]))
        for x in range(2):
            counter+=1
            beta_carbon=float((hncacb_list[x].split()[2]))
            carbon_list[counter].append(f'{alpha_carbon} {beta_carbon}')
            hnca_list2=[]
            hncacb_list2=[]
            with open(HNCA) as hnca_file:
                for hnca_values in hnca_file:
                    if hnca_values == '\n' or hnca_values.split()[0] == 'Assignment':
                        continue
                    hnca_carbon=float(hnca_values.strip().split()[2])
                    if hnca_carbon<(alpha_carbon+carbon_tolerance) and hnca_carbon>(alpha_carbon-carbon_tolerance):
                        hnca_list2.append(hnca_values)
            with open(HNCACB) as hncacb_file:
                      for hncacb_values in hncacb_file:
                          if hncacb_values == '\n' or hncacb_values.split()[0] == 'Assignment':
                              continue
                          hncacb_carbon=float(hncacb_values.strip().split()[2])
                          if hncacb_carbon<(beta_carbon+carbon_tolerance) and hncacb_carbon>(beta_carbon-carbon_tolerance):
                              hncacb_list2.append(hncacb_values)
            for values in hnca_list2:
                hnca_nitrogen2=float(values.strip().split()[1])
                hnca_hydrogen2=float(values.strip().split()[3])
                for values2 in hncacb_list2:
                    hncacb_nitrogen2=float(values2.strip().split()[1])
                    hncacb_hydrogen2=float(values2.strip().split()[3])
                    if hncacb_nitrogen2 < (hnca_nitrogen2+nitrogen_tolerance) and hncacb_nitrogen2 > (hnca_nitrogen2-nitrogen_tolerance) and hncacb_hydrogen2 < (hnca_hydrogen2+hydrogen_tolerance) and hncacb_hydrogen2 > (hnca_hydrogen2-hydrogen_tolerance):
                        if hncacb_nitrogen2 < (nhsqc_nitrogen+nitrogen_tolerance) and hncacb_nitrogen2 > (nhsqc_nitrogen-nitrogen_tolerance) and hncacb_hydrogen2 < (nhsqc_hydrogen+hydrogen_tolerance) and hncacb_hydrogen2 > (nhsqc_hydrogen-hydrogen_tolerance):
                            continue
                        i_minus_1[counter].append(values)
                        i_minus_1[counter].append(values2)
    counter=0
    for x,y in zip(i_minus_1,carbon_list):
        if x != []:
            if len(x) > 5:
                continue
            if counter < 1:
                file.write(f'{nhsqc_values.strip()}\t{y}\t{x[::2]}\n')
            counter+=1
            if counter > 1:
                file.write(f'\t\t\t\t{y}\t{x[::2]}\n')


def find_peaks():
    hnca_list=[]
    hncacb_list=[]
    with open(NHSQC) as nhsqc_file,open(match_table,'w') as file,open(i_table,'w') as i_table_file,open(i_minus_1_table,'w') as i_minus_1_table_file,open(overlapping_peaks_table,'w') as overlapping_peaks_table_file:
        for nhsqc_values in nhsqc_file:
            if nhsqc_values == '\n' or nhsqc_values.split()[0] == 'Assignment':
                continue
            nhsqc_nitrogen=float(nhsqc_values.strip().split()[1])
            nhsqc_hydrogen=float(nhsqc_values.strip().split()[2])
            with open(HNCA) as hnca_file:
                for hnca_values in hnca_file:
                    if hnca_values == '\n' or hnca_values.split()[0] == 'Assignment':
                        continue
                    hnca_nitrogen=float(hnca_values.strip().split()[1])
                    hnca_hydrogen=float(hnca_values.strip().split()[3])
                    if hnca_nitrogen < (nhsqc_nitrogen+nitrogen_tolerance) and hnca_nitrogen > (nhsqc_nitrogen-nitrogen_tolerance) and hnca_hydrogen < (nhsqc_hydrogen+hydrogen_tolerance) and hnca_hydrogen > (nhsqc_hydrogen-hydrogen_tolerance):
                        hnca_list.append(hnca_values)
            with open(HNCACB) as hncacb_file:
                for hncacb_values in hncacb_file:
                          if hncacb_values == '\n' or hncacb_values.split()[0] == 'Assignment':
                              continue
                          hncacb_nitrogen=float(hncacb_values.strip().split()[1])
                          hncacb_hydrogen=float(hncacb_values.strip().split()[3])
                          if hncacb_nitrogen < (nhsqc_nitrogen+nitrogen_tolerance) and hncacb_nitrogen > (nhsqc_nitrogen-nitrogen_tolerance) and hncacb_hydrogen < (nhsqc_hydrogen+hydrogen_tolerance) and hncacb_hydrogen > (nhsqc_hydrogen-hydrogen_tolerance):
                              if re.search('CB',hncacb_values) is not None or re.search('G',hncacb_values) is not None:
                                  hncacb_list.append(hncacb_values)
            if len(hnca_list) >= 3 and len(hncacb_list) >= 3:
                overlapping_peaks_table_file.write(nhsqc_values+'\n')
            elif len(hnca_list) == 2 and len(hncacb_list) == 2:
                i_minus_1_table_file.write(nhsqc_values+'\n')
                fun(hnca_list,hncacb_list,nhsqc_values,file,nhsqc_nitrogen,nhsqc_hydrogen)
            else:
                i_table_file.write(nhsqc_values+'\n')

            hncacb_list.clear()
            hnca_list.clear()

def search_file(question):
    found_flag=False
    with open(match_table) as file:
        for lines in file:
            if found_flag is True and re.search("\['\d+",lines.split()[0]) is None:
                found_flag=False
            if found_flag is True:
                print(lines)
            if question == lines.split()[1]:
                found_flag=True
                print(lines)

def main():
    find_peaks()
    while True:
        question=input('type in nitrogen shift: ')
        if question == 'quit':
            break
        search_file(question)
main()
