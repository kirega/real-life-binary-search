import csv
from time import time
import timeit

def generate_field_mappings(fields, data):
    """
    Get a mapping of the columns of interest
    :param fields: a list of the column headers
    :param data: list of the headers of the csv.
    :return:
    """
    mapping = {}
    fields = [f.replace(' ', '').lower() for f in fields]
    for index, field in enumerate(data):
        field_lower = field.replace(' ', '').lower()
        if field_lower in fields:
            # index = field_to_match.index(field_lower)
            mapping[field_lower] = index
    return mapping


# Perform the binary search

def binary_search(data, key, field):
    key = key.replace('-', '')
    if len(data) == 0:
        return "Empty data set"
    if len(data) == 1:
        if data[0][field].replace('-', '') == key:
            return data[0]
        return 'Not found'

    mid = len(data)//2

    if key == data[mid][field].replace('-', ''):
        return data[mid]

    if key < data[mid][field].replace('-', ''):
        return binary_search(data[0:mid], key, field)

    if key > data[mid][field].replace('-', ''):
        return binary_search(data[mid:], key, field)


def linear_search(data, key, field):
    key = key.replace('-', '')
    for row in data:
        if row[field] and row[field].replace('-', '') == key:
            return row

# Speed tests comparing the two algorithms with timeit


def binary_time():
    SETUP_CODE = '''
from __main__ import binary_search, generate_field_mappings
import csv'''
    TEST_CODE = '''
with open('client_data.csv', 'r') as f:
    client = csv.reader(f, delimiter=',')
    client_data = []
    for rec in client:
        client_data.append(rec)
field_map = generate_field_mappings(
    ['Client Name', 'Account No'], client_data[0])
result = binary_search(
    client_data[1:], '0001-0000-0069', field_map['accountno'])

   '''

    print('binary time', timeit.repeat(setup=SETUP_CODE,repeat=3,stmt=TEST_CODE, number=10000))

def linear_time():
    SETUP_CODE = '''
from __main__ import linear_search, generate_field_mappings
import csv'''
    TEST_CODE = '''
with open('client_data.csv', 'r') as f:
    client = csv.reader(f, delimiter=',')
    client_data = []
    for rec in client:
        client_data.append(rec)
field_map = generate_field_mappings(
    ['Client Name', 'Account No'], client_data[0])
result = linear_search(
    client_data[1:], '0001-0000-0069', field_map['accountno'])

   '''
    print("Linear time ->",timeit.repeat(setup=SETUP_CODE,repeat=3,stmt=TEST_CODE, number=10000))

if __name__ == '__main__':
    # load the data into memory

    with open('client_data.csv', 'r') as f:
        client = csv.reader(f, delimiter=',')
        client_data = []
        for rec in client:
            client_data.append(rec)
    field_map = generate_field_mappings(
        ['Client Name', 'Account No'], client_data[0])
    account_ids = []
    # for each in client_data[1:]:
    #     account_ids.append(each[field_map['accountno']])
    tt = time()
    result = binary_search(
        client_data[1:], '0001-0000-0069', field_map['accountno'])
    print(result)
    print("binary tt ->", time() - tt)

    dt = time()
    rst = linear_search(
        client_data[1:], '0001-0000-0069', field_map['accountno'])
    print(rst)
    print("linear tt ->", time() - dt)

    binary_time()
    linear_time()
