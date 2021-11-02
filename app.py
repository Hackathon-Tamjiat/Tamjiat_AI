from flask import Flask
from detect_2 import AI_Test
from flask import Flask ,render_template, request0
import ssl
from werkzeug.utils import secure_filename
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    name = "main('945669_41000_4928.jpg')"
    return name


@app.route('/ai_post',methods=['GET','POST'])
def post():
        path_dir = "../Tamjiat_Web/public/upload"
        file_list = os.listdir(path_dir)
        name = ""
        lists = request.form['file_name']
        uuid = request.form['cduuid']

        for i in file_list:
            if i == lists:
                name = i
        result = AI_Test(path_dir+"/"+ name)
        print("=============================")
        print(result)
        print("=============================")
        db= pymysql.connect(host=os.environ.get("DB_host"),
                     port=int(os.environ.get("DB_port")),
                     user=os.environ.get("DB_user"),
                     passwd=os.environ.get("DB_password"),
                     db=os.environ.get("DB_database"),
                     charset='utf8')
        cursor = db.cursor()
        if result=="정상" or result=="탐지불가":
            sql = "UPDATE userDcrop SET AICheck = '완료' , cdName = '"+result+"', iscdCheck='false' where cduuid = '"+uuid+"'"
        else:
            sql = "UPDATE userDcrop SET AICheck = '완료' , cdName = '"+result+"', iscdCheck='true' where cduuid = '"+uuid+"'"
        cursor.execute(sql)
        db.commit()
        db.close()
        return result

if __name__ == '__main__':
    ssl_context= ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='key_backup/server.crt',keyfile='key_backup/server.key')

    app.run(host='192.168.0.254',port=5002,debug=True,ssl_context=ssl_context)