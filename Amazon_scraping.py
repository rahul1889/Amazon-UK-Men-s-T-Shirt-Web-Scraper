#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# In[12]:


#function to extract the product title

def get_title(soup):
    
    try:
        title = soup.find("span", attrs={'id':'productTitle'})
        
        title_value = title.text
        
        title_string = title_value.strip()
        
    except AttributeError:
        title_string = ""
        
    return title_string
    
#function to extract the product price

def get_price(soup):
    
    try:
        price = soup.find("span", attrs={'class': 'a-price-whole'}).text.rstrip(".")
        
    except AttributeError:
        price = ""
        
    return price

#function to extract the product price

def get_rating(soup):
    
    try:
        rating = soup.find("span", attrs={'class':'a-icon-alt'}).text.strip()
    
    except AttributeError:
        rating = ""
        
    return rating

#function to extract review count

def get_reviews_counts(soup):
    
    try:
        review_count = new_soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.rstrip(" ratings")
        
    except AttributeError:
        
        review_count = ""
        
    return review_count

# function to extract the stock availability

def get_stock_info(soup):
    
    try:
        stock_check = new_soup.find("span", attrs={'class':'a-size-medium a-color-success'}).text.strip()
        
    except AttributeError:
        
        stock_check = ""
        
    return stock_check

    


# In[18]:


#main function

if __name__ == '__main__':
    
    #adding user agent in heading
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    
    #webpage URL 
    URL = "https://www.amazon.co.uk/s?k=men+t+shirts&ref=nb_sb_noss_1"
    
    
    #HTTP request
    webpage = requests.get(URL, headers = HEADERS)
    
    #Soup object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    #fetch links as list of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    
    #store the links in empty list
    links_list = []
    
    #loop for extracting links from tag objects
    for link in links:
        links_list.append(link.get('href'))
        
    d = {"title":[], "price":[], "rating":[], "reviews":[], "availability":[]}
    
    #loop for extracting product details from each link
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.co.uk" + link, headers = HEADERS)
        
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
        #function calls to display all product info
    
        d["title"].append(get_title(new_soup))
        d["price"].append(get_price(new_soup))
        d["rating"].append(get_rating(new_soup))
        d["reviews"].append(get_reviews_counts(new_soup))
        d["availability"].append(get_stock_info(new_soup))
    

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_extracted_data.csv", header = True, index=False)


# In[19]:


amazon_df


# In[ ]:




