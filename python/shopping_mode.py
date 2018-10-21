import time
import nltk
from time import sleep
from rev_ai import speechrec
from scraper import get_price
from decimal import Decimal
import citi

def get_account_balance():
    data = citi.get_checkings_info()
    return data['checkingAccount']['currentBalance']

result = []
total_cost = 0
time_elapsed = 0
transcript = ''
api_key = "01WQE3s0C3jia1Nwai6QNUwODAtnQvhB_2QJM3jeniUktT-pNoMtl91rlxqZmzqMtgG_e_wJdo2Shty7V-uEmwFdRIlsE"
voice = speechrec.RevSpeechAPI(api_key)

print "-----------------\n"
# response = voice.submit_job_local_file("shopping-3.mp4")
# id = 236922729
# id = 326429600 # rev.ai
id = 34486354  #mlh
# id = response['id']

print "Job created on rev.ai | ID: %s " % id

t0 = time.time()
status = voice.view_job(id)

while True:
    status = voice.view_job(id)
    print "Waiting for transcription | %d seconds elapsed" % time_elapsed

    if status['status'] == 'transcribed':
        print "Received transcription from rev.ai | %.2f seconds (total elapsed time)" % (time.time()-t0)
        rev_ai_output = voice.get_transcript(id, use_json=True)
        rev_ai_output = rev_ai_output['monologues'][0]['elements']

        for word in rev_ai_output:
            transcript += word['value']

        break

    sleep(10)
    time_elapsed += 10

print "Transcript: %s " % transcript

is_noun = lambda pos: pos[:2] == 'NN'
tokenized = nltk.word_tokenize(transcript)
nouns = [word.lower() for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
# print "Nouns: " + ', '.join(nouns) + "\n"

for noun in nouns:
    if noun != "afford" and noun != "pro" and noun != "prices" and noun != "price" and noun != "cost" and noun !="cost":
        price = get_price(noun)
        print "Cost of %s: %s " % (noun, price)
        result.append("Cost of %s: %s " % (noun, price))

        price = ''.join(c for c in price if c.isdigit() or c == '.')
        price = float(price)
        if price >= 0 and price <= 20000:
            total_cost += price

print "\nTotal cost: $%.2f " % total_cost
print "\n-----------------"

result.append("Total cost: $%.2f <br>" % total_cost)

total_balance = float(get_account_balance())
print total_balance
remaining_balance = float(total_balance - total_cost)
print total_cost
print remaining_balance
percent_cost = float(total_cost/total_balance)*100
result.append("Your remaining balance after this purchase will be $%.2f." % remaining_balance)
print float(total_cost/total_balance)*100

result.append("This purchase costs %.2f" % percent_cost + "% of your overall balance.")

if percent_cost > 25:
    result.append("This purchase leaves you with <u>too little</u> disposable income. Please consider removing some items.")


with open('../result_shopping_info.txt', 'w') as f:
    for item in result:
        f.write("%s\n<br>" % item)


