#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 21:42:48 2019

@author (comments): David Pokrajac
"""

""""
must use 127.0.0.1 on windows
pip install pymongo

"""
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)


def main():
    mongo = MongoDBConnection()

    with mongo: #Context manager.
        # mongodb database; it all starts here
        db = mongo.connection.media #We are connecting to a database named "media". 

        # collection in database
        cd = db["cd"] #Please do not confuse "cd" (corresponding to CompactDisk) with similarly named OS command (change directory)

        # notice how easy these are to create and that they are "schemaless"
        # that is, the Python module defines the data structure in a dict,
        # rather than the database which just stores what it is told

        cd_ip = {"artist": "The Who", "Title": "By Numbers"}
        result = cd.insert_one(cd_ip) #Inserting precisely one record

        cd_ip = [{
            "artist": "Deep Purple",
            "Title": "Made In Japan",
            "name": "Andy"
        },
                 {
                     "artist": "Led Zeppelin",
                     "Title": "House of the Holy",
                     "name": "Andy"
                 }, {
                     "artist": "Pink Floyd",
                     "Title": "DSOM",
                     "name": "Andy"
                 },
                 {
                     "artist": "Albert Hammond",
                     "Title": "Free Electric Band",
                     "name": "Sam"
                 }, {
                     "artist": "Nilsson",
                     "Title": "Without You",
                     "name": "Sam"
                 }] #List of dictionaries corresponding to records to be inserted

        result = cd.insert_many(cd_ip) #Inserts records specified in the list above

        print_mdb_collection(cd) #Prints all records from a specified table

        # another collection, i.e., table
        ThePersonWhoCollects = db["ThePersonWhoCollects"] #Should table names be the same or different?
        #I changed name from collector to ThePersonWhoCollects so that it would not be confused with "collection".
        ThePersonWhoCollects_ip = [{
            "name": "Andy",
            "preference": "Rock"
        }, {
            "name": "Sam",
            "preference": "Pop"
        }]
        result = ThePersonWhoCollects.insert_many(ThePersonWhoCollects_ip) #The database appears after we insert many

        print_mdb_collection(ThePersonWhoCollects)

        # related data
        for CurrentRecord in ThePersonWhoCollects.find(): #Here CurrentRecord is a variable pointing to each found record in a table
            #CurrentRecord is a dictionary (EACH record is a dictionary). We can refer an element of the dictionary
            #by its key; one of the keys is called "name"
            print(f'List for {CurrentRecord["name"]}')
            query = {"name": CurrentRecord["name"]}
            for a_cd in cd.find(query): #Find all the records from table "cd" where attribute name is equal to a specified value (which happens to be a
                #a name of a current record). In general, keys from records need satisfy properties specified in query
                print(f'{CurrentRecord["name"]} has collected {a_cd}')

        # start afresh next time?
        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            cd.drop()
            ThePersonWhoCollects.drop() #Deletes the table and the data


if __name__ == "__main__":
    main()