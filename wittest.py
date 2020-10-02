from wit import Wit
import json

wit_access_token = "IH6LCI4GFDC3GHAS635WBKUSYKWFY2MT"

wit_client = Wit(wit_access_token)


def getwit(message):

    resp = wit_client.message(message)

    print('Yay, got Wit.ai response: ' + str(resp))
    print ("****************************")
    # js = str(resp).replace("'", '"')
    # print (js)
    # jres = json.loads(js)

    intentlist = []
    contactnames = []
    numbers = []
    medications = []
    durations = []
    qdos = []
    slevels = []
    mbody = " "
    dt = []
    for i in resp['intents']:
        print (i)
        if 'name' in i:
            print (i['name'])
            intentlist.append(i['name'])
    print ("****************************")

    if 'wit$contact:contact' in resp['entities']: 
        for i in resp['entities']['wit$contact:contact']:
            print(i)
            contactnames.append(i['body'])
            # print(resp['entities']['wit$contact:contact'])
        
    if 'wit$number:number' in resp['entities']: 
        print ('numbers')
        for i in resp['entities']['wit$number:number']:
            print(i)
            numbers.append(i['body'])
    
    if 'medication:medication' in resp['entities']: 
        print ('medicines')
        for i in resp['entities']['medication:medication']:
            print(i)
            medications.append(i['body'])
    
    if 'wit$duration:duration' in resp['entities']: 
        print ('durations')
        for i in resp['entities']['wit$duration:duration']:
            print(i)
            durations.append(i['body'])
    
    if 'wit$quantity:quantity' in resp['entities']: 
        print ('dosage quantity')
        for i in resp['entities']['wit$quantity:quantity']:
            print(i)
            qdos.append(i['body'])
    
    if 'wit$volume:volume' in resp['entities']: 
        print ('dosage quantity')
        for i in resp['entities']['wit$volume:volume']:
            print(i)
            qdos.append(i['body'])

    if 'wit$message_body:message_body' in resp['entities']: 
        print ('message')
        for i in resp['entities']['wit$message_body:message_body']:
            print(i)
            mbody = mbody + " " +str(i['body'])
    
    if 'wit$datetime:datetime' in resp['entities']: 
        print ('datetime')
        for i in resp['entities']['wit$datetime:datetime']:
            print(i)
            dt.append(i['body'])
            
    
    if 'strictness_level:strictness_level' in resp['entities']: 
        print ('strictness')
        for i in resp['entities']['strictness_level:strictness_level']:
            print(i)
            slevels.append(i['body'])

    # for e in resp['entities']:
    #     print (e)
    #     if 'wit$contact:contact' in e:
    #         print (e[0])
    
    # entities = resp['entities']
    # intents = resp['intents']
    
    return intentlist, contactnames, numbers, medications, durations, qdos, slevels, mbody, dt


i, c , n, m, d, q, s, mess, dt = getwit("2 pm 6 pm and 8 pm")

print (i)
print (c)
print (n)
print (m)
print (d)
print (q)
print (s)
print (dt)
print (mess)







