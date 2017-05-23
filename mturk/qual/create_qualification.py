#copyright Martin McEnroe 2017
#MIT license

import boto3
import pprint

environ = 'prod'

if environ == 'sandbox':
    endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    my_results = 'results/sandbox_created_hits.txt'
    qual_preview_url = 'https://workersandbox.mturk.com/mturk/requestqualification?qualificationId={}'
elif environ == 'prod':
    endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
    my_results = 'results/production_created_hits.txt'
    qual_preview_url = 'https://www.mturk.com/mturk/requestqualification?qualificationId={}'
else:
    print('no environment defined')

client = boto3.client(
    service_name = 'mturk',
    endpoint_url = endpoint_url
)

# In Sandbox this always returns $10,000
user_balance = client.get_account_balance()
print("Your account balance is ${}".format(user_balance['AvailableBalance']))

#questions for qualification test
testFile = open("data/qualification_question_2.xml")
test_with_answers = testFile.read()
testFile.close()

#answers for qualification test
answerFile = open("data/qualification_answer_key_2.xml")
answer_key = answerFile.read()
answerFile.close()

name = 'Emotion vocabulary test #9'
qual_response = client.create_qualification_type(
    Name = name,
    Keywords='emotion, emoji, gentle_persuader',
    Description='With this qualification you will be able to work on simple HITs about emojis',
    QualificationTypeStatus = 'Active',
    #RetryDelayInSeconds=12, #default if not specified is no retry
    Test = test_with_answers,
    AnswerKey = answer_key,
    TestDurationInSeconds=120  #ample time, really
)

#might need some of the info like create timestamp
with open('data/qual_response.pickle', 'wb') as f:
    pickle.dump(qual_response, f)

#extract the qualificationTypeId for use in generating the HITs
qualification_type_id = qual_response['QualificationType']['QualificationTypeId']

print("Your qualification ID is: {}".format(qualification_type_id))
print(qual_preview_url.format(qualification_type_id))
