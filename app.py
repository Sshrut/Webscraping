from flask import Flask,render_template,request
import pickle
from bs4 import BeautifulSoup
import requests,html5lib,lxml
from urllib.request import urlopen
import re
import os



app=Flask(__name__)

def ans_result(user_str):
	splitstr=user_str.split(' ')
	user_input='+'.join(splitstr)
	search=requests.get("https://www.google.com/search?q=geeks+for+geeks+introduction+to+"+user_input).text
	soup=BeautifulSoup(search,'html.parser')

	new=soup.find('div',{'id':'main'})
	asdf=new.find('div',{'class':'kCrYT'})
	#print(new.prettify())
	
	need=str(asdf.a)
	if need=='None':
		new=soup.find('div',{'class':'BNeawe UPmit AP7Wnd'}).text
		l=new.split(' ')
		final_url='https://'+l[0]+'/'+l[2]

	else:
		ans=re.search("(?P<url>https?://[^\s]+)", need).group("url")
		final_url=ans.split(';')[0][:-5]

	#print(final_url)
	page=requests.get(final_url).text

	new_soup=BeautifulSoup(page,'html.parser')
	content=new_soup.find('div',{'class':'entry-content'})

	allresult=content.find_all('p')
	result=content.find('p').text

	ans_f=[]

	if result=='':
		flag=0
		for i in allresult:
			ans_f.append(i.text)
			flag+=1
			if flag==2:
				break
		final_ans=''.join(ans_f)
	else:
		final_ans=result

	return final_ans


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():

	int_feature=request.form['key']
	user_str=str(int_feature)
	final_result=str(ans_result(user_str))

	return render_template('index.html',answer=final_result)


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	query_result = req.get('queryResult')
	techn = query_result.get('parameters').get('technology')
	sum = getContent(techn)
	print('here num1 = {0}'.format(techn))
	
	return {
		"fulfillmentText": sum,
		"displayText": '25',
		"source": "webhookdata"
	}

if __name__=='__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
	