# Recap This Video For Me

In response to the Corona Virus Outbreak, we realized that there is a lot of information available on the internet and many of which are available in a video format but little to no ways of comiling all this information without having to watch all these videos which can both be time-consuming and mentally-straining. To solve this problem, we came up with 'Recap This Vid For Me' which utilizes Google's video intelligence API to transcribe the video into text and implements a custom-built unsupervised natural language processing algorithm, text rank, to summarize the key elements in the video by recognizing the most common sentences/ words.

# How we built it?

Front-end: HTML, CSS, Vanilla JS\
Back-end: Python, Google Cloud Video Intelligence API, cloud functions, pub/sub and cloud storage\
Natural Language Processing (NLP): NLTK, numpy, Networkx 

## Installation Instructions
```
1) Open your command prompt
2) Install python by following the instructions on https://wiki.python.org/moin/BeginnersGuide/Download and install a virtual environment
3) Open your command prompt 
4) Navigate into our project by using cd RecapThisVideo
5) Type 'cd Backend'
6) Type 'pip install -r requirements.txt'
7) Create a https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-gcloud and set it as an environment key
```

## Build and Run
```
1) Type 'python AsyncSetUp.py' by navigating to the backend of our project in your command prompt to run our API 
2) To only run the Video Transcriptions and Natural Language Processing scripts, type 'python VideoIntelligence.py' 
3) To only run the SendGrid script for sending out the results, type 'python SendResults.py' 
```
To find our serverless implementation, you can navigate to the following forked repository: https://github.com/StanfordLin/RecapThisVid.
