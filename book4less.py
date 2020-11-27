import requests
import getpass

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