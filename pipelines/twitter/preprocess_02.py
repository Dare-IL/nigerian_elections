import pandas as pd
import sys, os

nigerian_states = ['abia',
 'adamawa',
 'akwaibom',
 'anambra',
 'bauchi',
 'bayelsa',
 'benue',
 'borno',
 'crossriver',
 'delta',
 'ebonyi',
 'edo',
 'ekiti',
 'enugu',
 'gombe',
 'imo',
 'jigawa',
 'kaduna',
 'kano',
 'katsina',
 'kebbi',
 'kogi',
 'kwara',
 'lagos',
 'nasarawa',
 'niger',
 'ogun',
 'london', # add this before ondo
 'ondo',
 'osun',
 'oyo',
 'plateau',
 'rivers',
 'sokoto',
 'taraba',
 'yobe',
 'zamfara',
 'abuja']

def clean_states(x: str, nigerian_states: list)-> str:
    '''

    '''

    for s in nigerian_states:
        if s in x:
            return s
        
    return 'unknown'    

def prep_tweet(tweet: str) -> str:
    '''
    Preprocess tweet string based on Bert format
    '''

    # 
    tweet_words = []

    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)

    tweet_proc = " ".join(tweet_words)

    return tweet_proc

def create_candidate_party(tweet, config):    
    '''
    Check tweet for key words related to a particular candidate

    TODO: A tweet can be about multiple parties/candidates...
    
    '''
    for party, keywords in config.party_keywords.items():
        for word in keywords:
            if word in tweet:
                return party

    return None

def preprocess(config):
    '''
    
    '''
    data_processed = []
    for query in config.queries[config.candidate]:  
        q = query.replace('#', '').replace(' ', '')

        try:    
            data = pd.read_csv(f'{config.save_dir}/tweets_{q}.csv', encoding='utf-8')
        except FileNotFoundError:
            print(f'could not find {config.save_dir}/tweets_{q}.csv')
            sys.exit()

        # flag for if user in Nigeria
        data['in_nigeria'] = data['user_loc'].apply(lambda x: 'nigeria' in str(x).lower())

        # get/clean state  
        data['state'] = data['user_loc'].apply(lambda x:str(x).split(',')[0].lower())               
        data['state'] = data['state'].str.lower()  

        # remove unecessary symbols and white spaces
        for symbol in ['-', '_', ',', ' '] :
            data['state'] = data['state'].str.replace(symbol, '')

        # rename states  
        data['state'] = data['state'].str.replace('nigeria','')
        data['state'] = data['state'].str.replace('portharcourt','rivers')
        data['state'] = data['state'].str.replace('federalcapitalterritory','abuja')
        data['state'] = data['state'].apply(lambda x: clean_states(x, nigerian_states))

        # get candidate
        data['tweet'] = data['tweet'].str.lower()
        data['party_candidate'] = data['tweet'].apply(lambda x: create_candidate_party(x, config))
        

        # prepare tweet for sentiment analysis
        data['tweet_proc'] = data['tweet'].apply(lambda x: prep_tweet(x))            

        data_processed.append(data)
    
    # save intermediate file
    all_data = pd.concat(data_processed, ignore_index=True)
    all_data.to_csv(f'{config.save_dir}/{config.file_outputs.preprocess.name}_{config.candidate}.csv', index=False)    

    return