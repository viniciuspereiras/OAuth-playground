from flask import Flask, redirect, session, render_template, request, url_for
from flask_session import Session

from blueprints.auth import Authentication
from blueprints.info import userInfo

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    if not Authentication.check(session):
        return redirect('/login')
    
    if session['idp'] == 'google':
        try:
            user_info = userInfo.get_google_info(Authentication.getGoogleToken(session['google_authorization_code'])['access_token'])
        except KeyError:
            session['logged_in'] = False
            return redirect('/login')
        session['user_info'] = user_info


        
    return render_template('index.html', user_info=user_info)


@app.route('/login')
def login():
    if Authentication.check(session):
        return redirect('/')

    return render_template('login.html', url_google='/auth/google')

@app.route('/auth/google/')
def auth_google():
    auth_google = Authentication.authGoogle()
    google_url = auth_google['google_url']
    state = auth_google['state']
    session['state_oauth'] = state
    return redirect(google_url)
    
@app.route('/auth/google/callback')
def authGoogleCallback():
    if request.args.get('error') == 'access_denied':
        return 'You denied the request to login.'
    
    state = request.args.get('state')
    code = request.args.get('code')
    try:
        assert state == session['state_oauth']
    except:
        return 'Invalid state parameter.'
    
    session['google_authorization_code'] = code
    session['logged_in'] = True
    session['idp'] = 'google'
    return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



app.run(debug=True)
    