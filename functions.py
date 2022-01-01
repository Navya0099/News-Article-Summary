
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
from transformers import pipeline
import pickle


summarizer = pipeline("summarization")

def textextract2(url):
    address = url
    soup = BeautifulSoup(urlopen(address).read(), 'lxml')
    span = soup.find("div", {"class": "article__body-content"})
    paras = [x for x in span.findAllNext("p")]
    middle = "\n\n".join(["".join(x.findAll(text = True)) for x in paras[: -1]])
    return(middle)

def textextract1(url):
    y = " "
    url = urlopen(url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find("div",{"class":"ssrcss-uf6wea-RichTextComponentWrapper e1xue1i85"})
    paras = [x for x in table.findAllNext("p")]
    middle = "\n\n".join(["".join(x.findAll(text = True)) for x in paras[: -1]])
    return(middle)


def newextract(url):
    y = " "
    url = urlopen(url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find("div",{"class":"gel-layout__item gel-2/3@l"})
    paras = [x for x in table.findAllNext("p")]
    middle = "\n\n".join(["".join(x.findAll(text = True)) for x in paras[: -1]])
    return(middle)

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
        
    res = summarizer(chunks, do_sample=False)
    summary = ''.join([summ['summary_text'] for summ in res])
    
    return (summary)

with open('model_pkl', 'wb') as files:
    pickle.dump(summarizer, files)

