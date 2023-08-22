from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
import pandas as pd
import datetime
import sys

# labels = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}


def load_model():
    '''
    
    '''
    # load model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    return model, tokenizer

def get_sentiment(tweet_cleaned, model, tokenizer, config):
    '''
    
    '''      

    # sentiment analysis
    encoded_tweet = tokenizer(tweet_cleaned, return_tensors='pt')  
    # print(f'Calling model {datetime.datetime.now()}')  
    output = model(**encoded_tweet)
    # print(f'Received model output {datetime.datetime.now()}')  

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    # print(f'Scores = {scores}')

    sentiment = config.analysis.labels[np.argmax(scores)]

    return sentiment

def analysis(config):
    '''
    
    '''    
    
    try:    
        data = pd.read_csv(f'{config.save_dir}/{config.file_outputs.preprocess.name}_{config.candidate}.csv',encoding='utf-8') 
    except FileNotFoundError:
        print(f'could not find {config.save_dir}/{config.file_outputs.preprocess.name}_{config.candidate}.csv')
        sys.exit()

    print('loading model')
    model, tokenizer = load_model()

    start = datetime.datetime.now()
    print(f'Starting analysis {start}')       
    data['sentiment'] = data['tweet_proc'].apply(lambda x: get_sentiment(x, model, tokenizer, config))
    end = datetime.datetime.now()
    print(f'Finished analysis at {end} -> {end-start}')

    #Save output
    data.to_csv(f'{config.save_dir}/{config.file_outputs.analysis.name}_{config.candidate}.csv',encoding='utf-8', index=False)


    return
