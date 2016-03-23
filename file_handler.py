__author__ = 'a.ivanov'
import os
import csv
import datetime


def make_d(dir_list):
    for target_path in dir_list:
        try:
            os.mkdir(target_path)
        except OSError as data:
            if data.winerror != 183:
                print("Исключение %s." % data.strerror)
                input()
            pass


def format_float(value, elem_name):
    f_value = value.replace(',', '.').lstrip()
    # if value[0] == '0':
    #     f_value = value[1:]
    # else:
    #     f_value = value

    elem_pos = '%s\t' % elem_name
    return elem_pos + f_value + '\n'


analysis_path = 'C://temp//Analysis.txt'
analysis_result_path = 'C://temp//'
# analysis_path = 'C://Users//a.ivanov//Downloads//temp//Analysis.txt'
root_target_path = '//coredwire-pc//spectro//'
# root_target_path = 'C://Users//User3//Documents//temp//'
# root_target_path = 'C://Users//a.ivanov//Downloads//temp//'

with open(analysis_path, 'r') as analysis_file:
    analysis_file_entry = analysis_file.readlines()  # Содержимое файла, как совокупность строк разделенных \n
    f_name_prefix = analysis_file_entry[1].split()[
                        0] + '_'  # Первая часть имени (префикс) конечного файла выгрузки в формате ГГГГММДД_
    part_year = f_name_prefix[:4] + '//'  # Часть пути, характеризующая год выгрузки в формате ГГГГ
    # Часть пути, характеризующая месяц выгрузки в формате ГГГГ_ММ
    part_month = part_year[:4] + '_' + f_name_prefix[4:6] + '//'
    # Полный путь к дирректории назначения года
    target_path_dir_year = root_target_path + part_year
    target_path_dir_full = target_path_dir_year + part_month  # Полный путь к дирректории назначения месяца
    # Полный путь к дирректории года первичной записи результатов измерений
    analysis_path_dir_year = analysis_result_path + part_year
    # Полный путь к дирректории месяца первичной записи результатов измерений
    analysis_path_dir_full = analysis_path_dir_year + part_month
    target_f_name = f_name_prefix + 'analysis.txt'  # Имя файла согласно формату ГГГГММДД_analysis.txt

    make_d([analysis_path_dir_year, analysis_path_dir_full])

    target_analysis_path = analysis_path_dir_full + target_f_name
    target_path = target_path_dir_full + target_f_name

    # Реализовать протокол ITACA
    try:
        with open(target_analysis_path, 'r+') as target_f:
            # Если файл уже содержит записи, тогда писать данные только со второй строки analysis_file_entry

            if len(target_f.readlines()):

                for l in analysis_file_entry[1:]:
                    target_f.write(l)
                    # Если файл новый тогда писать файл целиком
            else:
                target_f.writelines(analysis_file_entry)
    except FileNotFoundError:
        with open(target_analysis_path, 'w+') as target_analysis_f:
            target_analysis_f.writelines(analysis_file_entry)

    reader = csv.DictReader(analysis_file_entry, delimiter=';')

    for row in reader:
        SampleTime = row['SampleTime']
        source_code = row['SourceCode'].strip()
        value_C = row['C']
        value_Si = row['Si']
        value_Mn = row['Mn']
        value_P = row['P']
        value_S = row['S']
        value_Cr = row['Cr']
        value_Cu = row['Cu']
        value_Mg = row['Mg']

    if source_code != 'F':
        try:
            spectro_to_promelt = analysis_result_path + 'telegram.txt'
            with open(spectro_to_promelt, 'a') as sp_to_promelt:
                dt_object = datetime.datetime.strptime(SampleTime, '%Y%m%d %H:%M:%S')
                dt_to_string = dt_object.strftime('%d-%b-%Y\t%H:%M\n')
                sc = '%s\n' % source_code.strip()
                number_of_elements = '8\n'
                stamp_C = format_float(value_C, 'C')
                stamp_Si = format_float(value_Si, 'Si')
                stamp_Mn = format_float(value_Mn, 'Mn')
                stamp_P = format_float(value_P, 'P')
                stamp_S = format_float(value_S, 'S')
                stamp_Cr = format_float(value_Cr, 'Cr')
                stamp_Cu = format_float(value_Cu, 'Cu')
                stamp_Mg = format_float(value_Mg, 'Mg')

                entry = '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}\n'.format('SCADA_DATA\n',
                                                                          sc, dt_to_string, number_of_elements,
                                                              stamp_C, stamp_Si, stamp_Mn, stamp_P, stamp_S, stamp_Cr,
                                                              stamp_Cu, stamp_Mg)
                sp_to_promelt.write(entry)

        except FileNotFoundError:
            pass

    # Полученный файл в из каталога измерений скопировать в одноименный файл в сетевом каталоге по адресу target_f_name
    with open(target_analysis_path, 'r') as analysis_f:
        make_d([target_path_dir_year, target_path_dir_full])
        with open(target_path, 'w')as target_f:
            target_f.writelines(analysis_f.readlines())

    # То же сделать для файла spectro_to_promelt.txt
    with open(spectro_to_promelt,'r') as spectro_source_f:
        with open(root_target_path + 'spectro_to_promelt.txt', 'w') as spectro_destination_f:
            spectro_destination_f.writelines(spectro_source_f.readlines())


if __name__ == '__main__':
    with open(target_path, 'r') as target_f:

        readlines_list = [row.split(';') for row in target_f]
        print_list = [readlines_list[0], readlines_list[len(readlines_list) - 1]]
        elements_q = len(print_list[0])
        x = []
        for i in range(elements_q - 1):
            x.append([elem[i].lstrip() for elem in print_list])

    print('Результаты записи:\n______________________________________')
    for row in x:
        print(row[0].rjust(12), ' - ', row[1])
    print('______________________________________')
    print('Данные успешно записаны и отправлены!')
    input()
