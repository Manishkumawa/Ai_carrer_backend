from flask import Flask,redirect,request,render_template ,jsonify,session,url_for

from pymongo import MongoClient
from gridfs import GridFS
import hashlib
from dotenv import load_dotenv
import os
from flask_oauthlib.client import OAuth
from flask_cors import CORS
load_dotenv()

from flask_mail import Mail ,Message
app = Flask(__name__)
CORS(app)



app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')

app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['AI_database']
fs = GridFS(db)


def calculate_hash(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()

@app.route('/carrer' ,methods = ['GET','POST'])
def carrer():

    if request.method =="POST":

        data = request.get_json()
        first_name = data.get('firstName')
        last_name  = data.get('lastName')
        email = data.get('email')
        phone = data.get('phone')
        address_line1 = data.get('address_line1')
        address_line2 = data.get('address_line2')
        city = data.get('city')
        hear_about = data.get('hear_about')
        past_employe = data.get('past_employe')
        pdf_file = request.files['resume']
        
        #my experinence
        data2 =request.get_json()
        company=data2.get("company")
        job_title=data2.get("job_title")
        start_date=data2.get("from")
        end_date=data2.get("to",None)
        currently_working = data2.get('currently_working')
        jd = data2.get('jd')

        #eduction
        data3 = request.get_json()
        school=data3.get("school")
        degree=data3.get("degree")
        fieldofstudy=data3.get("fieldofstudy","Not provided")
        start = data3.get('start_date')
        end_date = data3.get('end_date')


        # certificate
        certification = request.files['certificate']

        #skills
        skills = request.get_json()

        # website link
        weblink  = request.args.get('weblink','N/A')

        #social media links
        linkdin = request.args.get('linkdin','N/A')

        #github 
        github = request.args.get('github','N/A')

        

        # social media urls
        socials={'linkdin':linkdin ,'github':github,'weblink':weblink}

        # aplication questions 
        appQuestions =  request.get_json()



        pdf_content = pdf_file.read()
        pdf_hash = calculate_hash(pdf_content)

        if db.carrers.find_one({'hash':pdf_hash}):
            return jsonify({'message': 'Duplicate PDF file detected'}), 409
        
        file_id = fs.put(pdf_content, filename=pdf_file.filename)

        metadata = {
            'filename': pdf_file.filename,
            'hash': pdf_hash,
            'file_id': file_id
        }

        db.carrers.insert_one([{'personal_information':data },{'education':data3 },{'experience':data2},{'ALL Links':socials},{'Skills':skills},{'resume':metadata},{'Allquestion':appQuestions}])
    
        return redirect('/thank_you')
    return render_template('carrerPage.html')

@app.route('/thank_you')
def thank_you():
    
    return "Thankyou"  


@app.route('/applyWithLinkdin')
def applyWithLinkdin():

    return redirect('job linkdin url')



    


if __name__ =="__main__":
    app.run(debug =True)
