![](angel.png)

[![Robin](https://img.shields.io/badge/bot-angel-00B4FF.svg?style=for-the-badge)](https://angelassistant.tech)&nbsp;
[![Status](https://img.shields.io/badge/status-live-00B20E.svg?style=for-the-badge)](https://angelassistant.tech)&nbsp;

<!-- [![Donate](https://img.shields.io/badge/buy_me_coffee-donate-DFB217.svg?style=for-the-badge)](https://robin.silentbyte.com) -->

# Angel Assistant

Angel is an intelligent medication tracking assistant powered by [Wit.ai](https://wit.ai/). This project was submitted to the [Facebook Artificial Intelligence Hackathon](https://fbai2.devpost.com/) and [Facebook Messaging Hackathon](https://fbai2.devpost.com/).

Want to use Angel Assistant? Start a conversation by messaging at https://facebook.com/angelassistantai.

Our project website is https://angelassistant.tech/.

## Inspiration

Keeping track of personal medications is challenging for many people. According to a review in Annals of Internal Medicine, “studies have shown that 20 percent to 30 percent of medication prescriptions are never filled, and that approximately 50 percent of medications for chronic disease are not taken as prescribed.” This lack of adherence is estimated to cause approximately 125,000 deaths and at least 10 percent of hospitalizations, and to cost the American health care system between $100 billion and $289 billion a year.

Our team was determined to leverage the power of Wit.ai to build a well-designed and easy-to-use chatbot interface that assists people with remembering and keeping tracking of their medications, in an effort to encourage people to stay on top of their medications and remember to take them as prescribed. Angel Assistant supports a simple and accessible way for users to communicate via natural language and stay on top of their medications, which is possible through the cutting-edge infrastructure and technology of Wit.ai.

## What it does

Angel is an intelligent chatbot that allows users to quickly add, track, and remember their medications. Users can add medications via voice commands, specifying the name of the medicine, dosage, and times. They can update their status by leaving a quick voice or text message, after which Angel will give timely reminders. Lastly, Angel provides each patient with a unique ID, which they can then share with their doctors for them to monitor their patients’ progress, and send messages accordingly.

## How we built it

Angel lives in a Python based cloud server hosted on Azure. We are using Flask for the cloud server and MongoDB Atlas for our database. We are using the Facebook developer infrastructure to integrate the Angel Assistant backend with Messenger for automated intelligent messaging. 



Incoming messages from Messenger get forwarded to the Angel backend server for processing. 
Messages are then sent to our Wit.ai application, which returns the intent, state and traits of the message, backed by the mongoDB database and our state machine. In this manner, we curate custom responses to the user based on their message, as well as update the database accordingly.

## Challenges we ran into

The implementation of the chatbot logic and integration with Wit.ai was the most time consuming part because we had to set up the development environments and get everything functional before even starting. We also had challenges in implementing the voice commands features, as traditional Messenger voice audio files aren’t supported on the Wit.ai platform. Thus, we encoded and sent the data as .wav files over REST API. Lastly, migration of the bot from Flask to Azure functions was a challenge.

## Accomplishments that we're proud of

We were proud to have created a well-designed and well-executed Minimum Viable Prototype of an intelligent chat bot that successfully tracks medications, and implements various tracking features. The system integrates well with Messenger, and we strive to integrate it with other chat platforms as well in the future. Lastly, we are proud to have configured natural language interactions by enabling users to send custom voice messages.

## What we learned

We learned how to create concepts and intents in Wit.ai, and integrate it with a Flask backend server that sends messages to the Messenger platform. We learned how to create callback requests to our Flask backend server from the Messenger API infrastructure. Lastly, we wanted to transition our conventional Flask server to the more cost effective and efficient serverless architecture provided by Azure functions, which we learnt how to integrate with the python messenger client.

## What's next for Angel Assistant

Currently, Angel Assistant is designed and published as a Minimum Viable Product. We would like to refine the functionality, taking into consideration feedback from users and experts in the healthcare field. A feature we would especially like to implement is support for finding and showing further information on various medications, as well as integrating with pharmacy systems for online purchases of medications.


## References
* https://www.nytimes.com/2017/04/17/well/the-cost-of-not-taking-your-medicine.html
* https://pubmed.ncbi.nlm.nih.gov/22964778/


## Build Instructions

1. Set up your [Wit.ai](https://wit.ai/) and create [Messenger](https://developers.facebook.com/docs/messenger-platform/) bots to get your access keys.

2. Install Python and Flask via pip, and and update the access keys for the bot.

3. Start the ngrok server by running server.py.

4. Test using messenger

5. Alternatively, message https://facebook.com/angelassistantai to start chatting now!


