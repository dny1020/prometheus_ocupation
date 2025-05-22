# pylint: disable=C0114:missing-module-docstring
import csv


def read_csv(ruta):
    '''Read CSV file'''
    csv_list = []
    with open(ruta, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            csv_list.append(fila[0])

        return csv_list


def write_csv(ruta, lista, fieldnames):
    '''Write CSV file'''
    with open(ruta, mode='w', newline='', encoding='utf-8') as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for item in lista:
            writer.writerow(item)
