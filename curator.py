#!/usr/bin/python

import requests
import datetime
import time
import sys
from pprint import pprint
import os
import psutil

TUPLE_NAME = 0
TUPLE_DAYS_BOUNDARY = 1
DEFAULT_DAYS_BOUNDARY = 30

def get_configuration_file(list_days_boundary_by_indice):
    fd = open('curator_retention_conf.csv', 'Ur')
    for line in fd:
        if line in list_days_boundary_by_indice:
            continue
        else:
            list_days_boundary_by_indice.append(tuple(line.strip().split(':')))
    fd.close()
    return list(set(sorted(list_days_boundary_by_indice)))



def remove_indices(es_endpoint, list_indices, remove_elements):
    for element in remove_elements:
        delete = requests.delete(es_endpoint+list_indices[element])
        print ("Index removed: "+list_indices[element])

def search_old_indices(creation_times, list_indices, remove_elements):
    list_days_boundary_by_indice = []
    list_days_boundary_by_indice = get_configuration_file(list_days_boundary_by_indice)
    for i in range(0, len(list_days_boundary_by_indice)):
        current_time = int(time.time() * 1000)
        for j in range(0, len(creation_times)):
            offset = (1000 * 60 * 60 * 24 * int(list_days_boundary_by_indice[i][TUPLE_DAYS_BOUNDARY]))
            check_time = current_time - offset
            if check_time > int(creation_times[j]) and (list_indices[j][:len(list_days_boundary_by_indice[i][TUPLE_NAME])] == list_days_boundary_by_indice[i][TUPLE_NAME]):
                remove_elements.append(j)
            else:
                offset = (1000 * 60 * 60 * 24 * DEFAULT_DAYS_BOUNDARY)
                check_time = current_time - offset
                if check_time > int(creation_times[j]):
                    remove_elements.append(j)
    return list(set(sorted(remove_elements)))

def get_creation_time_indices(es_endpoint, list_indices, creation_times):
    for i in range(0, len(list_indices)):
        cdates = requests.get(es_endpoint+list_indices[i])
        cdates2 = cdates.json()
        creation_times.append(cdates2[list_indices[i]]['settings']['index']['creation_date'])
    return creation_times

def get_indices(es_endpoint, list_indices):
    indices = requests.get(es_endpoint+"_cat/indices")
    result = indices.text.split('\n')
    del result[-1]
    for lines in result:
        list_indices.append(lines.split()[2])
    if ".kibana-4" in list_indices:
        list_indices.remove(".kibana-4")
    elif ".kibana" in list_indices:
        list_indices.remove(".kibana")
    return sorted(list_indices)

def main(es_endpoint):
    list_indices=[]
    creation_times=[]
    remove_elements=[]
    es_endpoint = "http://"+es_endpoint+"/"

    list_indices = get_indices(es_endpoint, list_indices)
    creation_times = get_creation_time_indices(es_endpoint, list_indices, creation_times)
    remove_elements = search_old_indices(creation_times, list_indices, remove_elements)
    print (len(remove_elements))

#    process = psutil.Process(os.getpid())
#    print(process.memory_info().rss)

    for element in remove_elements:
        print ("Names of indexes who will be deleted: ", list_indices[element])
    print ("Numbers of indexes that will be deleted: ", len(remove_elements))
#    remove_indices(es_endpoint, list_indices, remove_elements)


if __name__ == "__main__":
    main(sys.argv[1])
