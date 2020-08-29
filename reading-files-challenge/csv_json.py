'''convert csv to json and change datatypes'''

#import all necessary dependences

import bz2
import csv
import json
from collections import namedtuple
from datetime import datetime

#This is where we define our tuple that consists of the tuple name, first item, and the field names, second item.
#src = the original name of each header; dest = the name we are changing the src to; concert = the datatype that we're converting the column to (i.e. int, float, str)
Column = namedtuple('Column', 'src dest convert')

#Since csv files only contain strings, here is a function that converts a string object to datetime
def parse_timestamp(text):
    return datetime.strptime(text, '%Y-%m-%d %H:%M:%S')

#here is where we define how we want to convert each column. The first item in each tuple refers to 'src'; 
#the second item of each tuple refers to 'dest'; third item refers to 'convert'
columns = [
    Column('VendorID', 'vendor_id', int),
    Column('passenger_count', 'num_passengers', int),
    Column('tip_amount', 'tip', float),
    Column('total_amount', 'price', float),
    Column('tpep_pickup_datetime', 'pickup time', parse_timestamp),
    Column('tpep_dropoff_datetime', 'dropoff time', parse_timestamp), 
    Column('trip_distance', 'distance', float),
]

#Here is a function that iterates through each record and making the necessary datatype conversions
def iterate_records(filename):
    #opens the compressed csv file
    with bz2.open(filename, 'rt') as f:
        #Defines the file's data as a dictionary of key, value pairs
        reader = csv.DictReader(f)
        #loop through each record of the data
        for line in reader:
            #create an empty dictionary contain key, value pairs for each record
            record = {}
            #Here we have a double for loop that will loop thru each column for each record
            for col in columns:
                #Now for each column, we're going to define the value of each record/line
                value = line[col.src]
                #While we're still on each column, we're going to convert the value and assign it to the corresponding key, which is represented 
                #by the 'dest' field name
                record[col.dest] = col.convert(value)
            #the function will return each record as its processed.
            yield record

#Because JSON files aren't able to support datetime objects, we need to create a function that converts datetime objects to a string
#before we dump all the records into a json file
def encode_time(obj):
    #if the obj isn't a datetime data type, return the obj as is
    if not isinstance(obj, datetime):
        return obj
    #if the obj is a datetime obj, then format it as a string
    return obj.isoformat()

#finally, we're going to tie all the functions together
#open a blank json file that we can write the new data to
with open('taxi.jl', 'w') as out:
    for record in iterate_records('taxi.csv.bz2'):
        #for each processed record, we'll going to dump it into a "data"
        data = json.dumps(record, default=encode_time)
        #write the data into the json file tht we defined as "out" and separate each record with a new line
        out.write(f'{data}\n')


