
from flask import Flask, render_template , request , jsonify
from bs4 import BeautifulSoup
import requests
import pandas as pd
app = Flask(__name__)
url = "https://in.bookmyshow.com/bengaluru/movies/kgf/ET00042769/critic-reviews"
l=[]
sauce = requests.get(url)
soup = BeautifulSoup(sauce.text,"html.parser")
critic_reviews = soup.find('div',id='mv-critic', class_='tab-content').find_all('div',class_='mv-synopsis-review')
for x in critic_reviews:
    data = {}
    data['Author'] = x.find('span',id="critic_",itemprop="author").text
    data['Ratings']= x.find('div', class_="__reviewer-name-rate").find('span' ,class_="__review-rate ").find('svg', class_="rated-review").get('data-value')
    data['Reviews'] = x.find('div' ,id="criticReview_" ,class_="__reviewer-text").find('span',itemprop="description").text
    l.append(data) 
df = pd.DataFrame(data=l)
df.to_csv('Movie_Ratings', index = True)
draft = pd.read_csv('Movie_Ratings',index_col=0).set_index('Author')


@app.route('/')
def index():
	return render_template('UserId.html')
	
@app.route("/UserData", methods =['POST','GET'])
def UserData():
	if request.method == 'POST':
		try:
			result = draft.loc[request.form['UserId']].to_dict()
			return render_template('Result.html',result=result)
		except:
			return '<H1>No Such Author</H1>'
	

if __name__ == '__main__':
	app.run()