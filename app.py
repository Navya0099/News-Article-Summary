from flask import Flask,render_template
import pandas as pd
import numpy as np
from flask import request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from transformers import pipeline
import os
from f import textextract2,textextract1,newextract

summarizer = pipeline("summarization")

cw = os.getcwd()
path = '/newslink'
ourPath = cw + os.path.join(path)

if(ourPath):
    os.chdir(ourPath)
    os.system('scrapy crawl news')

data = pd.read_json('newslinks.json', orient= 'dictionary')
# Filter the video content
data1 = data[data['heading'] != 'video']
data1.reset_index(inplace=True, drop= True)

diction = data1.to_dict()

x = np.array(data1['link'])
y = np.array(data1['title'])
z = np.array(data1['heading'])

newdf = pd.DataFrame(x, columns= ['Links'])
newdf['News Article Title'] = y
newdf['Heading'] = z
data1 = newdf[newdf['Heading'] != 'video']
data1.reset_index(inplace=True, drop= True)


os.chdir(cw)


def generate_summary(inp_str):
    max_chunk = 500
    inp_str = inp_str.replace('.', '.<eos>')
    inp_str = inp_str.replace('?', '?<eos>')
    inp_str = inp_str.replace('!', '!<eos>')
    
    sentences = inp_str.split('<eos>')
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
        
    res = summarizer(chunks, max_length = 70, min_length = 10, do_sample=False)
    summary = ''.join([summ['summary_text'] for summ in res])
    
    return (summary)


list1 = {}

for i in range(len(x)):
    try:
        list1[data1['Links'][i]]=textextract1(data1['Links'][i])
    except:
        try:
            list1[data1['Links'][i]]=textextract2(data1['Links'][i])
        except:
            try:
                list1[data1['Links'][i]]=newextract(data1['Links'][i])
            except:
                pass

df = pd.DataFrame(list1.items(), columns=['Links', 'Text'])
cv =pd.merge(df, data1, on='Links')

for i in range(0,len(cv)):
    if cv['Heading'][i][:4] == 'hero':
        cv['Heading'][i] = 'Head'
    else :
        pass

viewdf = cv[['Links','News Article Title']]

app = Flask(__name__)

@app.route('/')  

def home():
    return render_template('home.html', tables=[viewdf.to_html(classes='data',render_links=True,escape=False)], titles=viewdf.columns.values)


@app.route('/summary', methods = ['GET','POST'])
def summary():

    if request.method == 'POST':
        summarydf = pd.DataFrame()
        if request.form['action'] == 'Check Headlines Summary':
            f = cv.loc[cv['Heading'] == 'Head'][['Text','News Article Title']]
            f['Summary'] = f['Text'].apply(generate_summary)
            f.drop('Text', axis =1, inplace= True)
            summarydf = f.copy()
        elif request.form['action'] == 'Check News & Sports Summary':
            d = cv[cv['Heading'].isin(['news','sport'])][['Text','News Article Title']]
            d['Summary'] = d['Text'].apply(generate_summary)
            d.drop('Text', axis =1, inplace= True)
            summarydf = d.copy()
        elif request.form['action'] == 'Check Indian News Summary':
            g = cv.loc[cv['Heading'] == 'regional-news'][['Text','News Article Title']]
            g['Summary'] = g['Text'].apply(generate_summary)
            g.drop('Text', axis =1, inplace= True)
            summarydf = g.copy()
        elif request.form['action'] == 'Check Editor Choice Summary':
            h = cv.loc[cv['Heading'] == 'editors-picks'][['Text','News Article Title']]
            h['Summary'] = h['Text'].apply(generate_summary)
            h.drop('Text', axis =1, inplace= True)
            summarydf = h.copy()
        elif request.form['action'] == 'Check More BBC News':
            j = cv.loc[cv['Heading'] == 'more-bbc'][['Text','News Article Title']]
            j['Summary'] = j['Text'].apply(generate_summary)
            j.drop('Text', axis =1, inplace= True)
            summarydf = j.copy()
        elif request.form['action'] == 'Check Special News':
            k = cv[cv['Heading'].isin(['secondary-special-features','primary-special-features','features-and-events'])][['Text','News Article Title']]
            k['Summary'] = k['Text'].apply(generate_summary)
            k.drop('Text', axis =1, inplace= True)
            summarydf = k.copy()
        else:
            pass

    return render_template('summary.html',tables=[summarydf.to_html(classes='data',escape=False)], titles=summarydf.columns.values)


if __name__ == '__main__':
    app.run(debug=True)
