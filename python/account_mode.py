import time
import citi
import nltk
from time import sleep
from rev_ai import speechrec
from scraper import get_price

result = []
total_cost = 0
time_elapsed = 0
transcript = ''
api_key = "01WQE3s0C3jia1Nwai6QNUwODAtnQvhB_2QJM3jeniUktT-pNoMtl91rlxqZmzqMtgG_e_wJdo2Shty7V-uEmwFdRIlsE"
voice = speechrec.RevSpeechAPI(api_key)

print "-----------------\n"
# response = voice.submit_job_local_file("accounts-2.mp4")
# id = 519584099
id = 24532463 # testing amount spent in last few months
# id = response['id']
transcript = ''


def get_account_balance():
    data = citi.get_checkings_info()
    return data['checkingAccount']['currentBalance']

def get_interest_amount():
    data = citi.get_checkings_info()
    return data['checkingAccount']['totalInterestAmount']

def get_last_statement_date():
    data = citi.get_checkings_info()
    return data['checkingAccount']['lastStatementDate']

def get_payment_due_date():
    data = citi.get_credit_info()
    return data['creditCardAccount']['paymentDueDate']

def get_credit_limit():
    data = citi.get_credit_info()
    return data['creditCardAccount']['creditLimit']

def get_minimum_due_amount():
    data = citi.get_credit_info()
    return data['creditCardAccount']['minimumDueAmount']

def where_do_i_go():
    data = citi.get_credit_transactions()
    transactions = data['transactions']
    #   maps places to how many times a transaction took place there
    timesVisited = {}
    for transaction in transactions:
        place = transaction['transactionDescription']
        if place in timesVisited:
            timesVisited[place] = timesVisited[place] + 1
        else:
            timesVisited[place] = 1

    mostOftenPlace = "Nowhere"
    mostTimes = 0
    for place in timesVisited:
        if timesVisited[place] > mostTimes:
            mostOftenPlace = place
            mostTimes = timesVisited[place]

    return mostOftenPlace, mostTimes


def where_spend_most_money():
    data = citi.get_credit_transactions()
    transactions = data['transactions']

    #   maps places to how many times a transaction took place there
    priceMapping = {}
    for transaction in transactions:
        place = transaction['transactionDescription']
        amountSpent = transaction['transactionAmount']
        if place in priceMapping:
            priceMapping[place] = priceMapping[place] + amountSpent
        else:
            priceMapping[place] = amountSpent

    mostExpensivePlace = "Nowhere"
    highestCost = 0
    for place in priceMapping:
        if priceMapping[place] > highestCost:
            mostExpensivePlace = place
            highestCost = priceMapping[place]

    return mostExpensivePlace, highestCost

def amount_spent_in_past():
    #   array at increments for 1 month, 3 months, half year, 1 year, and 2 years
    amounts_spent = {'1' : 0, '3' : 0, '6' : 0, '12' : 0, '24' : 0}

    data = citi.get_credit_transactions()
    transactions = data['transactions']

    for transaction in transactions:
        date = transaction['transactionDate']
        # year and month for this transaction
        year = int(date[0:4])
        month = int(date[5:7])
        days = int(date[8:10])
        # find out how many months ago it was
        monthsAgo = abs(2018 - year) + abs(10 - month)
        daysAgo = monthsAgo * 30 + days
        # go through list of months, and add if applicable
        for amount in amounts_spent:
            if daysAgo <= amount * 30:
                amounts_spent[amount] += int(transaction['transactionAmount'])

    # for amount in amounts_spent:
    #     print(str(amount) + " " + str(amounts_spent[amount]));

    #   return dictionary of months ago -> amount spent before that time
    return amounts_spent

print "Job created on rev.ai | ID: %s " % id

t0 = time.time()
status = voice.view_job(id)

while True:
    status = voice.view_job(id)
    # print status
    print "Waiting for transcription | %d seconds elapsed" % time_elapsed

    if status['status'] == 'transcribed':
        # result.append("Received transcription from rev.ai | %.2f seconds (total elapsed time)" % (time.time()-t0))
        print "Received transcription from rev.ai | %.2f seconds (total elapsed time)" % (time.time()-t0)
        rev_ai_output = voice.get_transcript(id, use_json=True)
        rev_ai_output = rev_ai_output['monologues'][0]['elements']

        for word in rev_ai_output:
            transcript += word['value']

        break

    sleep(10)
    time_elapsed += 10

print "Transcript: %s" % transcript

result.append("Transcript: " + transcript + "<br>")

transcript = transcript.lower()

if "account balance" in transcript or "accounts balance":
    print("Your current account balance is $" + str(get_account_balance()))
    result.append("Your current account balance is $" + str(get_account_balance()))

if "interest amount" in transcript:
    print("Your current interest amount is $" + str(get_interest_amount()))
    result.append("Your current interest amount is $" + str(get_interest_amount()))

if "last statement" in transcript:
    print("Your last statement was due on the date " + str(get_last_statement_date()))
    result.append("Your last statement was due on the date " + str(get_last_statement_date()))

if "next payment is due" in transcript or "last payment was" in transcript:
    print ("Your next payment is due on the date " + get_payment_due_date())
    result.append("Your next payment is due on the date " + get_payment_due_date())

if "credit limit" in transcript:
    print ("Your maximum credit limit is $" + str(get_credit_limit()))
    result.append("Your maximum credit limit is $" + str(get_credit_limit()))

if "minimum due amount" in transcript:
    print("The minimum amount due is $" + str(get_minimum_due_amount()))

if "where do i spend" in transcript:
    place, money = where_spend_most_money()
    print("You spend the most amount of money at " + str(place) + " ($" + str(money) + ")")
    result.append("You spend the most amount of money at " + str(place) + " ($" + str(money) + ")")

if "where do i go" in transcript:
    place, numVisited = where_do_i_go()
    print("You have spent most frequently at " + str(place) + " (" + str(numVisited) + " times)")
    result.append("You have spent most frequently at " + str(place) + " (" + str(numVisited) + " times)")

if "in the last" in transcript:
    result2 = amount_spent_in_past()

    if "24" in transcript or "twenty four" in transcript or "twenty-four" in transcript:
        string = "You have spent $"
        string += str(result2['24'])
        string += " in the last 24 months."
        result.append(string)

    if "1" in transcript or "one" in transcript:
        string = "You have spent $"
        string += str(result2['1'])
        string += " in the last 1 month."
        result.append(string)

    if "3" in transcript or "three" in transcript:
        string += str(result2['3'])
        string += " in the last 3 months."
        result.append(string)

    if "12" in transcript or "twelve" in transcript:
        string = "You have spent $"
        string += str(result2['12'])
        string += " in the last 12 months."
        result.append(string)

    if "6" in transcript or "six" in transcript:
        string = "You have spent $"
        string += str(result2['6'])
        string += " in the last 6 months."
        result.append(string)


print "\n-----------------"

with open('../result_accounts_info.txt', 'w') as f:
    for item in result:
        f.write("%s\n<br>" % item)
