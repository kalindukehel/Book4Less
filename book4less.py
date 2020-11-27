import requests
import getpass
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sys

with requests.Session() as s:
    #get cookies from website
    pre_load = s.get('https://myfit4less.gymmanager.com/portal/booking/')

    #get Fit4Less credentials from user
    emailaddress = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    data = {
        'emailaddress' : emailaddress,
        'password' : password,
    }

    #Log into website and get active session
    response = s.post(
        'https://myfit4less.gymmanager.com/portal/login_done.asp',
        data=data
    )

    if(response.url == 'https://myfit4less.gymmanager.com/portal/login_failed.asp'):
        print("Invalid login.")
        sys.exit(1)

    #Get date and parse to search website for block
    date_input = input("Enter the date and time to book(dd-mm-yyyy hh:mm AM/PM): ")
    date_object = datetime.strptime(date_input, '%d-%m-%Y %I:%M %p')
    data_slotdate = str(date_object.strftime('%A')) + ', ' + str(date_object.day) + ' ' + str(date_object.strftime('%B')) + ' ' + str(date_object.year)
    data_slottime = 'at ' + str(date_object.strftime('%-I')) + ":" + str(date_object.strftime('%M')) + " " + str(date_object.strftime("%p"))
    
    #Input parsed data into a dictionary
    day_change_data = {
        'action':'daychange',
        'block_id': str(date_object.strftime('%Y-%m-%d')),
        'block_name':''
    }

    #Send post requst with parsed data to change to requested day
    second_req = s.post(
        'https://myfit4less.gymmanager.com/portal/booking/submit.asp',
        data=day_change_data
    )

    soup = BeautifulSoup(second_req.content,'html.parser')

    try:
        #Get block based on date and time
        block = soup.find(attrs={'data-slotdate':data_slotdate, 'data-slottime':data_slottime})

        block_id = block.get('id')
        block_id = block_id[block_id.index("_")+1:]

        block_club = block.get('data-slotclub')

        
        #Input parsed block data into a dictionary
        book_data = {
            'action': 'booking',
            'block_id': block_id,
            'block_name' : block_club + ' , ' + data_slotdate + ', ' + data_slottime
        }

        #Send post request with parsed data to book time
        book_response = s.post(
            'https://myfit4less.gymmanager.com/portal/booking/submit.asp',
            data=book_data
        )

        if(book_response.url == 'https://myfit4less.gymmanager.com/portal/booking/index.asp'):
            print("Successfully booked!")
        else:
            print("There was an error booking.")
    except:
        print("The date you entered is not valid for booking or it has not opened up yet!")
        print(data_slotdate,data_slottime)