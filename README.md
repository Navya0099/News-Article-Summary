# News-Article-Summary




## App preview (Home Page)
![image](https://user-images.githubusercontent.com/49746090/147853503-c3c2c6ea-6349-43f4-9484-c0d023b80938.png)

### Summary Page 
![image](https://user-images.githubusercontent.com/49746090/147853484-bcacd84b-d1e9-4134-98ca-c0812d18ed34.png)



Aim : This app is created to summarize and provide the gist of the news articles on the news website. This reduces the user's amount of time spent to 
read the all the articles & user can look into summary to find intresting news to scroll down and read full.


This App Uses scrapy in the backend to scrape the links from BBC Home Page.

The articles in the link are scraped using beautiful soup and articles are collected in the text format.
Hugging phase transformer's summarizer pipeline is used to create the summary of the collected articles and they are displayed on the 
webpage seperately based on the category of the news article.

Hugging phase transformers are pre-trained on cnn/daily news papers and provides the abstract summary of articles, unlinke extractive summary possible through
traditional ML methoods.

All this happens dynamically, as the BBC news page updates..!
