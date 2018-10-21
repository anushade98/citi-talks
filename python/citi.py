import requests
import uuid
import json

#   this access token is specific to a certain citi user, they have to have logged in w/user&pass
#   this one is using sandbox user 5!!!
access_token = "Bearer " + "AAIkNWUzODc5NGQtYzYyZi00NzYyLWFkMGItZjA0OWY2NTg0MGVhf_ckLXwQd39cIxJmZWRVjBDINPRadGpoIMUKTJN33FpUmObLCSXMfSIASgtPfZCuOoNGzQZBiG3-PpXIEglKLaTZZv3lxyQTDRHlvrgHu5LeBi3xktK8Z-XcePjr5huwvpZi-HBwcRznE19JebbPvivDj76LNgM6ifR1ybEnOlpMZUQNR8icGJDsYcQBSGlPTIJORdy7wxvU5PPtJqSwvDiIUvhI0wsnQPA4nln8fL_qlY97ThRqbX-8IeHFZpoD8qnebsipLk8XizxSmbLsLXbWVP3M3crW5qMfzlMavvfYDGI4sXmGcVpGGQFHX1O_nJYCU54YLaHE7CayQJ5CAprRU0V71p8TH-504UygsIFVYVV2wKV77sBa9GREzfYbbSRbTlla7VePWp-7We5oxQ"
client_id = "5e38794d-c62f-4762-ad0b-f049f65840ea"
uuid = str(uuid.uuid1())

url = "https://sandbox.apihub.citi.com/gcb/api/"
headers = {
        'accept' : 'application/json',
        'authorization' : access_token,
        'uuid' : uuid,
        'client_id' : client_id
    }

#response = requests.get(url, headers=headers)
#print(response.status_code)
#print(response.text)

def get_all_accounts():
    endpoint = "v1/accounts"
    response = requests.get(url + endpoint, headers=headers)
    # print(response.status_code)
    return response.text

    
def get_account_info(account_id):
    endpoint = "v1/accounts/" + str(account_id)
    response = requests.get(url + endpoint, headers=headers)
    # return response.status_code
    # print response.text
    return json.loads(response.text)

#   not really working
#   MUST BE IN YYYY-MM-DD format, from past 2 years
def get_account_transactions(account_id, start_date, end_date):
    endpoint = "v1/accounts/" + str(account_id) + "/transactions"
    params= 'transactionFromDate=' + start_date + '&transactionToDate=' + end_date
    response = requests.get(url + endpoint, headers=headers, params=params)
    # print(response.status_code)
    return json.loads(response.text)

def get_account_transactions(account_id):
    endpoint = "v1/accounts/" + str(account_id) + "/transactions"
    params= 'transactionFromDate=2016-10-20&transactionToDate=2018-10-20'
    response = requests.get(url + endpoint, headers=headers, params=params)
    # print(response.status_code)
    return json.loads(response.text)

def get_checkings_id():
    return 2016225123

def get_credit_card_id():
    return 2016569046

def refresh_token(refresh_token):
    thisHeader = {
            'accept': 'application/json',
            'authorization' : 'Basic NWUzODc5NGQtYzYyZi00NzYyLWFkMGItZjA0OWY2NTg0MGVhOk8ybVYxeU03clk4YUgxaVEzY1A2ZEIwdkcyblM1Z1k2YUI1ck44b1Yxbko0d0gzeEoy',
            'content-type' : 'application/x-www-form-urlencoded'
        }
    data = 'grant_type=refresh_token&refresh_token=' + refresh_token
    url = 'https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/refresh'
    response = requests.post(url, headers=thisHeader, data=data)
    print(response.status_code)
    print(json.loads(response.text))
    
def get_credit_transactions():
    credit_id = get_credit_card_id()
    return get_account_transactions(credit_id)
    
def get_checkings_info():
    checkings_id = get_checkings_id()
    return get_account_info(checkings_id)

def get_credit_info():
    credit_id = get_credit_card_id()
    return get_account_info(credit_id)

# refresh_token('AAL7iG7lHGpeOsjBWdxzQjTblIR1qvrjw9UyP4CHoDm5G9CtzrSKAHuLGOPl_ebx-T9VKnKnzc3CEAVFXvO9UMCCJPM0h_Ib93Lus5gEcSse0HyK5DV1ri_pOKIfAPL_zoNtPQfA4JGV9kTa8CE0LgFhj0OrmYyhjZ_Uj-lYrI3p60IMp8w1JdFd6XpbVapwewAfsRNo9oQ5Vc6LabEJeLKeUV4NuMkQHgtXyHv1-bo61JxexzrJZD5DHu2H0p26hLdboSWiTFiXMvs3roP8eeGwnUSnfqK0NzUSRu88oTf9e9uA7qA_3WyzEF4LP-DmnG5aVfzMtpIR0jO-giJKD4hMIdnjG7Z_GDHVJr-2GCp-9mhlM4GSnBPkSNqC_xOwwr5vnCUgb1TWHYcLZLD9CbQT')

# '''
# initial_data = b'5e38794d-c62f-4762-ad0b-f049f65840ea:O2mV1yM7rY8aH1iQ3cP6dB0vG2nS5gY6aB5rN8oV1nJ4wH3xJ2'
# encoded = base64.b64encode(initial_data)
#
# data = "grant_type=authorization_code&code=AALqYZRiBDbxMGkZlg-ov9Mu-AjsoQ4EnjaXm7XY6X50zlCphKD1Xl9CtU3tKWAtJ-t9wPRPb-9OiOgrl2uKS0DQknNNa7dAis9agb-Egy3BsEPVaGo3fBC8bXDqTiEqpYcc6dFgUKFw4dQ9Mae6MZ7AP4KSw3fO2kpHtyZlkk29PRcVZf7I6LTlEG9C_boJa8f2TM60x8EiaMXwkv7xTtM0fv583gmKJBX8DMcy68O5F0sqPeyartAIsbjv1gAG-UxOxP426D5NTiDoDNIzp7VNtgnfbs0vCOojYO50FmtUJjgWO6uEewGa_MGQDoy9BoE&redirect_uri=https://www.google.com/"
# #print(encoded)
# #data = "5e38794d-c62f-4762-ad0b-f049f65840ea:O2mV1yM7rY8aH1iQ3cP6dB0vG2nS5gY6aB5rN8oV1nJ4wH3xJ2".encode()
#
#
#
# headers = {
#     'accept': "application/json",
#     'authorization': 'Basic NWUzODc5NGQtYzYyZi00NzYyLWFkMGItZjA0OWY2NTg0MGVhOk8ybVYxeU03clk4YUgxaVEzY1A2ZEIwdkcyblM1Z1k2YUI1ck44b1Yxbko0d0gzeEoy',
#     'content-type': "application/x-www-form-urlencoded"
#     }
#
# #response = requests.post('https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/authorize?response_type=code&client_id=5e38794d-c62f-4762-ad0b-f049f65840ea&scope=accounts_details_transactions customers_profiles&countryCode=US&businessCode=GCB&locale=en_US&state=12093&redirect_uri=https://www.google.com/')
# response = requests.post('https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/token/au/gcb', data=data, headers=headers)
# print(response.status_code)
# print(response.text)
#
# def main():
#     global record
#     record = ""
#     audio = open('audio.mp3', 'rb')
#     record = audio.read(65536)
#     audio.close()
#     audio = open('audio.mp3', 'wb')
#     audio.write(record)
#     audio.close()
#
# main()'''