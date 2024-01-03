from flask import Flask, request, jsonify, render_template
from flask import Flask, g, session, redirect, request, url_for, jsonify, render_template
import requests
from dotenv import dotenv_values
from requests_oauthlib import OAuth2Session
import os

DOMAIN = os.environ.get('DOMAIN')
OAUTH2_REDIRECT_URI = f'{DOMAIN}/callback'
OAUTH2_CLIENT_ID = os.environ.get('DISCORD_OAUTH2_CLIENT_ID')
OAUTH2_CLIENT_SECRET = os.environ.get('DISCORD_OAUTH2_CLIENT_SECRET') # config[]
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = f'{API_BASE_URL}/oauth2/authorize'
TOKEN_URL = f'{API_BASE_URL}/oauth2/token'
GUILD_ID = os.environ.get('GUILD_ID')
INTRA_LOGIN_URL = os.environ.get('INTRA_LOGIN_URL')
PORT = os.environ.get('PORT') or '8000'




def token_updater(token):
    session['oauth2_token'] = token

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET
if 'http://' in OAUTH2_REDIRECT_URI:
    app.config['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', link=INTRA_LOGIN_URL)

@app.route('/rejected', methods=['GET'])
def rejected():
    return render_template('rejected.html')


def get_user(token):
    user = requests.get('https://api.intra.42.fr/v2/me', headers={
        'Authorization': f'Bearer {token}'
    })
    return user.json()

def get_coalition(user_id, token):
    coalition = requests.get(f'https://api.intra.42.fr/v2/users/{user_id}/coalitions', headers={
        'Authorization': f'Bearer {token}'
    })
    return coalition.json()

def get_token(code)->str:
    code = request.args.get('code')
    if not code:
        return 'no code'
    url = 'https://api.intra.42.fr/oauth/token'
    uid = os.environ.get('INTRA_ID')
    secret = os.environ.get('INTRA_SECRET')
    try: 
        res = requests.post(url, data={
            'grant_type': 'authorization_code',
            'client_id': uid,
            'client_secret': secret,
            'code': code,
            'redirect_uri': os.environ.get('INTRA_REDIRECT_URI')
        })
        return res.json()['access_token']
    except Exception as e:
        return ''


@app.route('/auth', methods=['GET'])
def auth():
    token = get_token(request.args.get('code'))
    user = get_user(token)
    coalition = get_coalition(user['id'], token)
    if coalition[0]['name'] == 'Freax':
        scope = request.args.get(
            'scope',
            'identify guilds.join')
        discord = make_session(scope=scope.split(' '))
        authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
        session['oauth2_state'] = state
        return redirect(authorization_url)
    else:
        #INFO: el bourki meme should be returned here
        return redirect('/rejected')





def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)


def add_to_guild(access_token, userID, guildID):
    url = f"{API_BASE_URL}/guilds/{guildID}/members/{userID}"
    botToken = os.environ.get('TOKEN')
    data = {
    "access_token" : access_token,
    }
    headers = {
    "Authorization" : f"Bot {botToken}",
    'Content-Type': 'application/json'
    }
    response = requests.put(url=url, headers=headers, json=data)
    return redirect(f'https://discord.com/channels/{guildID}/general')

@app.route('/callback')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    api = make_session(token=token)
    user = api.get(f'{API_BASE_URL}/users/@me').json()
    user_id = user.get('id')
    return add_to_guild(token.get('access_token'), user_id, GUILD_ID)
