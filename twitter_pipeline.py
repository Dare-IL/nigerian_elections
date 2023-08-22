from modulefinder import EXTENDED_ARG
import os, sys
import click
from dotenv import load_dotenv
from datetime import datetime, time
import pandas as pd

from helpers import read_config, make_data_dirs, get_latest_dir
from pandas import date_range
from pipelines.twitter.extract_01 import get_tweets
from pipelines.twitter.preprocess_02 import preprocess
from pipelines.twitter.sentiment_analysis_03 import analysis
from pipelines.twitter.visualisation_04 import create_visuals

load_dotenv()
api_key = os.getenv('api_key')


@click.command()
@click.option('--query',  type=click.Choice(['general', 'obi', 'tinubu', 'atiku']), help='query type for api. See yml', default='general')
@click.option('--end', help='date tweet published before', default=None)
@click.option('--config', help='configuration file', default='config.yml')
def main(query: str, end: str, config: str):    
    
    # TODO: if end date specified ensure it is later than start date
    if end:                
        until = "{}-{}-{}".format(end[:4],end[4:6],end[6:])
    else:
        until = datetime.today().date()    
        end =  str(until).replace('-','')   

    start = pd.to_datetime(end) - pd.DateOffset(days=6)
    start = str(pd.to_datetime(start).date()).replace('-','')  
    # read config    
    config = read_config(config)
    config['start']  = start
    config['end']   = end
    config['until']   = until
    config['candidate'] = query

    # execute pipeline steps in the following order
    pipeline_steps = ['extract', 'preprocess', 'analysis', 'output']
    pipeline_functions = {
        'extract': get_tweets, # 1. get data from twitter api
        'preprocess': preprocess, # 2. clean tweets and user location
        'analysis': analysis, # 3. classify tweet as +ve, -ve, or neutral
        'output': create_visuals # 4. create bar and pie charts
    }

    if 'extract' in config.pipeline_steps and config.pipeline_steps.extract: 
        # TODO: check for api keys        
        # make data directories to store extracted data
        save_dir = make_data_dirs(start, end) 
    else:        
        save_dir =  get_latest_dir()
        print(f'saving data in {save_dir}')

    config['save_dir'] = save_dir

    for step in pipeline_steps:
        if step in config.pipeline_steps and config.pipeline_steps[step]:  
            print(f'Starting {step} step')  
            pipeline_functions[step](config)
        else:
            print(f'Skipping {step} step')        

if __name__ == '__main__':
    main()