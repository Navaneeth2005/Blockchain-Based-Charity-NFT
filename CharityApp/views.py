from django.shortcuts import render
from datetime import datetime
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import json
from web3 import Web3, HTTPProvider
import base64

global username, auctionList, bidList, usersList
global contract, web3

#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Charity.json' #Charity contract file
    deployed_contract_address = '0x40c085d972690dbCfff834Fd4a7997ac7c8338Ff' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getUsersList():
    global usersList, contract
    usersList = []
    count = contract.functions.getUserCount().call()
    for i in range(0, count):
        person = contract.functions.getPersonname(i).call()
        phone = contract.functions.getPhone(i).call()
        email = contract.functions.getEmail(i).call()
        password = contract.functions.getPassword(i).call()
        utype = contract.functions.getUserType(i).call()
        usersList.append([person, phone, email, password, utype])

def getBidList():
    global bidList, contract
    bidList = []
    count = contract.functions.getBidCount().call()
    for i in range(0, count):
        auction_id = contract.functions.getBidAuctionId(i).call()
        bidder = contract.functions.getBidder(i).call()
        amount = contract.functions.getAmount(i).call()
        bid_date = contract.functions.getBidDate(i).call()
        transaction = contract.functions.getTransactionType(i).call()
        bidList.append([auction_id, bidder, amount, bid_date, transaction])

def getAuctionList():
    global auctionList, contract
    auctionList = []
    count = contract.functions.getAuctionCount().call()
    for i in range(0, count):
        auction_name = contract.functions.getAuctionName(i).call()
        auction_id = contract.functions.getAuctionId(i).call()
        auction_details = contract.functions.getAuctionDetails(i).call()
        price = contract.functions.getMinimumAmount(i).call()
        start_date = contract.functions.getStartDate(i).call()
        end_date = contract.functions.getEnddate(i).call()
        category = contract.functions.getCategory(i).call()
        auctionList.append([auction_name, auction_id, auction_details, price, start_date, end_date, category])
getUsersList()
getBidList()    
getAuctionList()
print(bidList)

def DonateAction(request):
    if request.method == 'POST':
        global bidList, username
        auction_id = request.POST.get('t1', False)
        price = request.POST.get('t2', False)
        donate = request.POST.get('t3', False)
        card = request.POST.get('t4', False)
        cvv = request.POST.get('t5', False)
        transaction = request.POST.get('t6', False)
        print(transaction)
        current_date = str(datetime.now().date())
        msg = contract.functions.saveBid(auction_id, username, donate, current_date, transaction).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        bidList.append([auction_id, username, donate, current_date, transaction])
        context= {'data':'Your '+transaction+' Accepted with below Blockchain Transaction details<br/><br/>'+str(tx_receipt)}
        return render(request, 'UserScreen.html', context) 

def Donate(request):
    if request.method == 'GET':
        global username
        auction_id = request.GET['aid']
        amt = request.GET['amt']
        output = '<tr><td><font size="3" color="black">Auction&nbsp;ID</td><td><input type="text" name="t1" size="15" value="'+auction_id+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Minimum&nbsp;Amount</td><td><input type="text" name="t2" size="15" value="'+amt+'" readonly/></td></tr>'
        context= {'data1':output}
        return render(request,'Donate.html', context)

def checkDate(start_date,end_date):
    status = False
    current_date = datetime.now().date()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    print(str(start_date)+" "+str(end_date)+" "+str(current_date))
    print((current_date >= start_date))
    print((current_date <= end_date))
    if current_date >= start_date and current_date <= end_date:
        status = True
    return status

def BrowseList(request):
    if request.method == 'GET':
        global auctionList, username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Auctioner Name</font></th>'
        output+='<th><font size=3 color=black>Auction ID</font></th>'
        output+='<th><font size=3 color=black>Auction Details</font></th>'
        output+='<th><font size=3 color=black>Minimum Amount</font></th>'
        output+='<th><font size=3 color=black>Start Time</font></th>'
        output+='<th><font size=3 color=black>End Time</font></th>'
        output+='<th><font size=3 color=black>Category</font></th>'
        output+='<th><font size=3 color=red>Click to Donate/Bid</font></th></tr>'
        for i in range(len(auctionList)):
            alist = auctionList[i]
            date_status = checkDate(alist[4], alist[5])
            if date_status:
                output+='<tr><td><font size=3 color=black>'+alist[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+alist[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+alist[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+alist[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+alist[4]+'</font></td>'
                output+='<td><font size=3 color=black>'+alist[5]+'</font></td>'
                output+='<td><font size=3 color=black>'+alist[6]+'</font></td>'
                output+='<td><a href=\'Donate?aid='+alist[1]+'&amt='+alist[3]+'\'><font size=3 color=red>Click Here</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'UserScreen.html', context)

def ParticipateAction(request):
    if request.method == 'POST':
        global bidList, username
        auction_id = request.POST.get('t1', False)
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Auction ID</font></th>'
        output+='<th><font size=3 color=black>Bidder Name</font></th>'
        output+='<th><font size=3 color=black>Bid Amount</font></th>'
        output+='<th><font size=3 color=black>Bid Date</font></th>'
        output+='<th><font size=3 color=black>Cause Category</font></th></tr>'
        amount = 0
        for i in range(len(bidList)):
            blist = bidList[i]
            if blist[0] == auction_id:
                amount += float(blist[2])
                output+='<tr><td><font size=3 color=black>'+blist[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+blist[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+blist[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+blist[3]+'</font></td>'
                output+='<td><font size=3 color=black>'+blist[4]+'</font></td></tr>'
        output+='<tr><td><font size=3 color=blue>Total Collected Amount = '+str(amount)+'</font></td></tr>'        
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'AuctionerScreen.html', context)           

def ViewParticipate(request):
    if request.method == 'GET':
        global auctionList, username
        output = '<tr><td><font size="3" color="black">Choose&nbsp;Auction&nbsp;ID</td><td><select name="t1">'
        for i in range(len(auctionList)):
            alist = auctionList[i]
            if alist[0] == username:
                output += '<option value="'+alist[1]+'">'+alist[1]+'</option>'
        output += '</select></td></tr>'
        context= {'data1':output}
        return render(request, 'ViewParticipate.html', context)  

def AddAuctionAction(request):
    if request.method == 'POST':
        global auctionList, username
        auction_details = request.POST.get('t1', False)
        price = request.POST.get('t2', False)
        start_date = request.POST.get('t3', False)
        end_date = request.POST.get('t4', False)
        category = request.POST.get('t5', False)
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        start_date = str(start_date.strftime("%Y-%m-%d"))
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        end_date = str(end_date.strftime("%Y-%m-%d"))
        auction_id = str(len(auctionList) + 1)
        msg = contract.functions.saveAuction(username, auction_id, auction_details, price, start_date, end_date, category).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        auctionList.append([username, auction_id, auction_details, price, start_date, end_date, category])
        context= {'data':'Auction details added to Blockchain with ID = '+str(auction_id)+'<br/><br/>'+str(tx_receipt)}
        return render(request, 'AddAuction.html', context)       

def AddAuction(request):
    if request.method == 'GET':
        return render(request,'AddAuction.html', {})

def index(request):
    if request.method == 'GET':
        return render(request,'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})
    
def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        global usersList
        person = request.POST.get('t1', False)
        phone = request.POST.get('t2', False)
        email = request.POST.get('t3', False)
        password = request.POST.get('t4', False)
        usertype = request.POST.get('t5', False)
        status = "none"
        for i in range(len(usersList)):
            users = usersList[i]
            if email == users[2]:
                status = "exists"
                break
        if status == "none":
            msg = contract.functions.saveUser(person, phone, email, password, usertype).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            usersList.append([person, phone, email, password, usertype])
            context= {'data':'Signup Process Completed<br/>'+str(tx_receipt)}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'Register.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        page = "UserLogin.html"
        for i in range(len(usersList)):
            ulist = usersList[i]
            user1 = ulist[2]
            pass1 = ulist[3]
            utype = ulist[4]
            if user1 == username and pass1 == password:
                status = "success"
                if utype == "Auctioner":
                    page = "AuctionerScreen.html"
                if utype == "Bidder/Donor":
                    page = "UserScreen.html"
                break
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, page, context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, page, context)
        










        


        
