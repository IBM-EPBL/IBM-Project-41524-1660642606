from flask import Flask,render_template,url_for,request
import inputScript
#import pymongo
from passlib.hash import  pbkdf2_sha256
import json
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "46QJ_oRgPFuE2UcGhsleCwXBIk4R_m0unM7a87psbKT9"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__,template_folder='templates')


@app.route("/")
def helloworld():
    return render_template("/home.html")

@app.route("/predicturl")
def predicturl():
    return render_template("/predict1.html")


@app.route("/predict" ,methods=["POST","GET"] )

def predict():
    url = request.form['url']
    checkprediction = inputScript.main(url)
    
    print(url)
    print(checkprediction)
    

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f9','f10','f11','f12','f13','f14','f15','f15','f16','f17','f18','f19','f20','f21','f22','f23','f24','f25','f26','f27']], "values":checkprediction }]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/62efb8db-e32e-4c70-bd7c-7f819762d9b7/predictions?version=2022-11-12', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred = response_scoring.json()
    output = pred['predictions'][0]['values'][0][0]
     
    
    if output==1 :
        return render_template("/output1.html")
    
    elif output==-1 :
        return render_template("/output.html")

@app.route("/project_details")
def support():
    return render_template("/project_details.html")

@app.route("/addurl")
def addurl():
    return render_template("/addurl.html")

@app.route("/about")
def about():
    return render_template("/about.html")


if __name__ =="__main__":
    app.run(debug=True)