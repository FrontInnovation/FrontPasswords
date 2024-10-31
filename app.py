from flask import Flask, request, redirect, url_for, session, render_template, g, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
from supporting_functions import *
from datetime import datetime
#import sys

#sys.path.append("C:\Users\filip\HTTPS")



app = Flask(__name__)
app.secret_key = '#FrontInnovation1234567890##FrontInnovation1234567890##FrontInnovation1234567890#'  # Set to a unique, secret value
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10000 per day", "1000 per hour"]
)

#Login route
#By default displayig the login.html page
#@limiter.limit("500 per day")
@app.route("/", methods=['GET', 'POST']) 
def index():
    if request.method == "POST":
        session.pop('username', None) #By default pops session
        username = request.form['username']
        password = request.form['password']

        if validate_credentials(username, password): #Checks username and password in login.db
            session['username'] = username #Starts session if the user is valid
            string = f"{username} successfully logged in; {datetime.now()}\n" #Written to log
            write_to_log(string) #Log
            return redirect(url_for('dashboard')) #Routes to /dashboard
    
        string = f"{username} tried to log in, but is not verified; {datetime.now()}\n"
        write_to_log(string)
    return render_template('login.html')


#@limiter.limit("500 per day")
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if 'username' in session: #g is global variable for user
        return render_template('dashboard.html')
    
    return redirect(url_for("index"))


#Route loggs out the user
@app.route('/logout')
def logout():
    try:
        username = session['username']
        session.pop('username', None)
        string = f"{username} successfully logged out; {datetime.now()}\n"
        write_to_log(string)
    except:
        return redirect(url_for("index"))

    return redirect(url_for("index"))
    #return render_template('login.html')


#@limiter.limit("500 per day")
@app.route("/getdata", methods=['GET'])
def getdata():
    if g.user:
        selskapsnavn = request.args.get("data")
        selskapsnavn = format_company_identifier(selskapsnavn)
        try: 
            orgnr = int(selskapsnavn) #checking if the orgnr is an 
            _, data = get_company_data_by_orgnumber(selskapsnavn)
            username = session['username'] #logging purposes
            string = f"{username} got data for: {selskapsnavn}; {datetime.now()}\n" # for the log
            write_to_log(string) #writes to log
            return json.dumps(data)
        
        except:
            data = get_company_data(selskapsnavn)
            username = session['username'] #logging purposes
            string = f"{username} got data for: {selskapsnavn}; {datetime.now()}\n" # for the log
            write_to_log(string) #writes to log
            return json.dumps(data)
    
    return redirect(url_for('index'))


#@limiter.limit("500 per day")
@app.route("/updatedata", methods=['POST'])
def updatedata():
    if g.user:
        if request.method == "POST":
            for element in request.form:
                if element == "" or element == " ":
                    return render_template("dashboard.html")
                            
            companyname, data = convert_reqest_to_datalist(request)
            companyname = format_company_identifier(companyname)
            try:
                if int(companyname): #if user searched by orgnumber
                    orgnr = companyname
                    compname, _ = get_company_data_by_orgnumber(orgnr)
                    update_company_data(compname, data)
                    username = session['username'] #logging purposes
                    string = f"{username} updated data for: {companyname}; {datetime.now()}\n" #for the log
                    write_to_log(string) # writes to log
                    return render_template('dashboard.html')
            except: #if user is looked up by companyname
                update_company_data(companyname, data)
                username = session['username'] #logging purposes
                string = f"{username} updated data for: {companyname}; {datetime.now()}\n" #for the log
                write_to_log(string) # writes to log
                return render_template('dashboard.html')
            
    return redirect(url_for('index'))


#get new company info and inserts into database
@app.route("/addnewinfo", methods=["POST"])
def addcompany():
    if g.user:
        if request.method == "POST":
            for element in request.form:
                if element == "" or element == " " or len(request.form['orgnr']) != 9:
                    return render_template("dashboard.html")
                
            #print(request.form)
            orgnr = request.form['orgnr']
            companyname = request.form['navn']
            data = [f"{request.form['stotteord']};{request.form['username']};{request.form['pass']}"]

            if get_company_data_by_orgnumber(orgnr) != None: # if company already exists and we add stotteordning to company 
                compname, compdata = get_company_data_by_orgnumber(orgnr)
                #if compname == companyname:
                compdata.append(data[0])
                update_company_data(companyname, compdata)
                username = session['username'] #logging purposes
                string = f"{username} updated data for: {companyname}; {datetime.now()}\n" #for the log
                write_to_log(string) # writes to log
                return render_template('dashboard.html')
            else: # company does not exist, and we add company to database
                add_new_company_data(orgnr, companyname, data)
                username = session['username'] #logging purposes
                string = f"{username} added new company: {companyname}; {datetime.now()}\n" #for the log
                write_to_log(string) # writes to log
                return render_template('dashboard.html')
    
    return redirect(url_for('index'))
    

#Preproccessing for each request
@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        g.user = session['username']


#Postprocessing for each request
@app.after_request
def after_request(response):
    #Deny browser to store page in cache, this is a safety feature
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0') 
    return response



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="443", ssl_context=('https/cert.pem', 'https/key.pem'))
    #app.run(host="10.0.0.204", port="443", ssl_context=('https/cert.pem', 'https/key.pem'))
