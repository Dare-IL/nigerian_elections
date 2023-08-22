import pandas as pd
import datetime
import sys
from box import Box
# import matplotlib.pyplot as plt

candidate_name_map = {'obi': 'Peter Obi', 'tinubu': 'Bola Tinubu', 'atiku': 'Atiku Abubakar'}

def create_visuals(config: Box, top_n: int = 5) -> None:
    '''
    Create bar and pie chart using data from sentiment analysis
    Args:
        config: project config which specifies intermediate csv file names with relevant data
        top_n: for barch chart, how many regions (ordered by no of tweets) to show
    '''    


    try:    
        data = pd.read_csv(f'{config.save_dir}/{config.file_outputs.analysis.name}_{config.candidate}.csv',encoding='utf-8') 
    except FileNotFoundError:
        print(f'could not find {config.save_dir}/{config.file_outputs.analysis.name}_{config.candidate}.csv')
        sys.exit()

    start, end = data['date'].min(), data['date'].max()
    start = pd.to_datetime(start).strftime('%Y/%m/%d')
    end = pd.to_datetime(end).strftime('%Y/%m/%d')
    month = datetime.datetime.strptime(end, '%Y/%m/%d').strftime("%B")#[:3]   
    name = candidate_name_map[config.candidate ]

    # aggregate tweets by state and sentiment 
    data_agg = data.groupby(['state', 'sentiment']).agg({'tweet_proc': 'count'}).unstack()

    # rename columns
    data_agg.columns = data_agg.columns.get_level_values(1)

    data_agg['total_tweets']= data_agg.sum(axis=1)
    data_agg = data_agg.fillna(0)

    # sort by total tweets to that regions with most tweets are at the top
    data_agg = data_agg.sort_values(by='total_tweets', ascending=False)
    pie_data = data_agg.sum()

    queries = data['query'].unique()
    title = "States with most tweets (search terms: " + ", ".join(queries) + ')'

    color_list = ['r', 'b', 'g']
    
    # only plot top_n regions
    fig1 = data_agg[['Negative', 'Neutral', 'Positive']].head(top_n).plot.bar(stacked=True,color=color_list, title=title).get_figure()
    fig1.savefig(f'{config.save_dir}/{config.candidate}_sentiment_by_state_{config.start}_{config.end}.png', bbox_inches='tight')
    fig1.clear()

    title2 = f'Sentiment of {int(pie_data["total_tweets"])} tweets about {name} in {month}'
    fig2 = pie_data[['Negative', 'Neutral', 'Positive']].plot.pie(colors=color_list,autopct='%1.1f%%', title=title2, ylabel='').get_figure()
    fig2.savefig(f'{config.save_dir}/{config.candidate}_sentiment_pie_chart_{config.start}_{config.end}.png', bbox_inches='tight')
    fig2.clear()


    return