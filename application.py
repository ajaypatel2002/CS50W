import os
import requests
import datetime

from flask import Flask, jsonify, render_template, request, url_for, session, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_session import Session

from collections import deque

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

channelsAvailable = []
usersLogged = []
channelWiseMessages =dict()
current_user_data={}

@app.route("/", methods=["POST", "GET"])
def index():
    entry=0
    try:

        if session.get("username") is None:
            return redirect("/signin")
        else:
            username=session['username']
        
            if session.get("current_channel") is None:
                return redirect("/channel_menu")
            else:
                selected_channel=session['current_chennel']
                
                return render_template("index.html",username=username,channels= channelsAvailable,selected_channel=selected_channel)
    except:
        return redirect("/signin")
        
@app.route("/signin",methods=["POST", "GET"])
def signin():
    
    session.clear()
    username = request.form.get("username")
    
    if request.method == "POST":
        if username in usersLogged:
            return render_template("error.html", message="username already exists! Please Try other username Please!")                   
        else:
            usersLogged.append(username)
            session['username'] = username
            session.permanent = True
            return redirect("/")        
    else:
        message="Welcome to gappa maar please sign in your name"
        return render_template("signin.html",message=message)

@app.route("/logout")#methods=["POST","GET"])
def logout():
    try:
        username=session.get('username')
        current_channel=session.get('current_channel')
        now = datetime.datetime.now()
        timenow = now.strftime("%d/%m-%H:%M")
        temp_msg=username + ' has logged out from this channel...'
        data={'user': username,'timenow': timenow,'msg': temp_msg}
        socketio.emit('status', data,broadcast=True)

        temp_channelWiseMessages_users=channelWiseMessages[channel]["users"]
        if username in temp_channelWiseMessages_users :
            temp_channelWiseMessages_users.remove(username)

        if "msgs" in channelWiseMessages[current_channel]:
            temp_channelWiseMessages=channelWiseMessages[current_channel]["msgs"]
            len(temp_channelWiseMessages)
                            
            add_msg={(list(temp_channelWiseMessages)[-1])+1: [username,timenow,temp_msg]}
            temp_channelWiseMessages.update(add_msg)
            if len(temp_channelWiseMessages)>100:
                temp_channelWiseMessages.pop((list(temp_channelWiseMessages)[-1])-100)
        
        session.pop('username', None)
        session.clear()    # Delete cookie    
        return redirect("/")
    except:
        return redirect("/signin")
#==============================

@app.route("/channel_menu")
def channel_menu():
    if session.get("username") is None:
        return redirect("/signin")
    else:
        return render_template("channel_menu.html", message="Please Select or Creat channel To Enjoy Chat!",channels = channelsAvailable)

@app.route("/create_channel", methods=['GET','POST'])
def create():
    # Get channel name from form
    newChannel = request.form.get("channel")
    username=session.get('username')
    now = datetime.datetime.now()
    msg_time = now.strftime("%d/%m-%H:%M")
    
    if request.method == "POST":
        if newChannel in channelsAvailable:
            return render_template("error.html", message="that channel already exists!")
        else:
            channelsAvailable.append(newChannel) # Add channel to list of channels
            channelWiseMessages[newChannel]={}
            if "channel_name" in channelWiseMessages:
                channelWiseMessages[newChannel]["channel_name"].append(newChannel)
            else:
                channelWiseMessages[newChannel]["channel_name"] = []
                channelWiseMessages[newChannel]["channel_name"].append(newChannel)

            channelWiseMessages[newChannel]["users"] = [username] 
            channelWiseMessages[newChannel]["msgs"] = {}
            welcome_msg={1: [username,msg_time,username+"Created this channel.., Welcome to this channel...,"]}

            if "msgs" in channelWiseMessages[newChannel]:
                temp_channelWiseMessages=channelWiseMessages[newChannel]["msgs"]
                temp_channelWiseMessages.update(welcome_msg)
            else:
                channelWiseMessages[newChannel]["msgs"]=welcome_msg
            return redirect("/channels/" + newChannel)
    else:
        return render_template("create_channel.html", channels = channelsAvailable)

@app.route("/leave_channel")
def leave_channel():
    try:
        username=session.get('username')
        current_channel=session.get('current_channel')
        now = datetime.datetime.now()
        timenow = now.strftime("%d/%m-%H:%M")
        temp_msg=username + ' has logged out from this channel...'
        data={'user': username,'timenow': timenow,'msg': temp_msg}
        socketio.emit('status', data,broadcast=True)


        temp_channelWiseMessages_users=channelWiseMessages[channel]["users"]
        if username in temp_channelWiseMessages_users :
            temp_channelWiseMessages_users.remove(username)

        if "msgs" in channelWiseMessages[current_channel]:
            temp_channelWiseMessages=channelWiseMessages[current_channel]["msgs"]
            len(temp_channelWiseMessages)
                            
            add_msg={(list(temp_channelWiseMessages)[-1])+1: [username,timenow,temp_msg]}
            temp_channelWiseMessages.update(add_msg)
            if len(temp_channelWiseMessages)>100:
                temp_channelWiseMessages.pop((list(temp_channelWiseMessages)[-1])-100)

        return redirect("channel_menu")
    except:
        return redirect("channel_menu")

@app.route("/channels/<channel>", methods=['GET','POST'])
def enter_channel(channel):
    try:
        entry=0
        #print(f"============================{session.get['username']}====after adding channel====")
        current_user_data["current_channel"]=channel
        session['current_channel'] = channel
        current_user_data["current_user_name"]=session['username']
        
        session.permanent = True
        username=session['username']
        now = datetime.datetime.now()
        msg_time = now.strftime("%d/%m-%H:%M")

        #join(channel)

            #========================== Show channel page to send and receive messages """
        if 'username' in session :
            # Updates user current channel
            if request.method == "POST":
                return redirect("/")
            else:
                temp_channelWiseMessages_users=channelWiseMessages[channel]["users"]
            
                if username in temp_channelWiseMessages_users :
                    print("this user is avialable")
                else:
                    temp_channelWiseMessages_users.append(username)
                    
                    if "msgs" in channelWiseMessages[channel]:
                        temp_channelWiseMessages=channelWiseMessages[channel]["msgs"]
                        len(temp_channelWiseMessages)
                        
                        w_msg="New Member " + username+" Logged in to this channel..."

                        welcome_msg={(list(temp_channelWiseMessages)[-1])+1: [username,msg_time,"New Member " + username+" Logged in to this channel..."]}
                        temp_channelWiseMessages.update(welcome_msg)

                        if len(temp_channelWiseMessages)>100:
                            temp_channelWiseMessages.pop((list(temp_channelWiseMessages)[-1])-100)

                        current_user_data["current_channel"]=channel


                        data={'user': username,'timenow': msg_time,'msg': w_msg}
                        socketio.emit('status', data,broadcast=True)

                    

                return render_template("index.html", channels= channelsAvailable, messages=channelWiseMessages[channel],entry=1)#,new_string=new_string)
        else:
            return redirect("/signin")
    except KeyError as error:
        return redirect("/channel_menu")

@socketio.on("join", namespace='/')
def join(channel):
    #""" Send message to announce that user has entered the channel """
    # Save current channel to join channel.
    #channel = session.get('current_channel')
    #join_room(channel)

    emit('status', {
        'userJoined': session.get('username'),
        'channel': channel,
        'msg': session.get('username') + ' has entered the channel'}, 
        channel=channel,broadcast=True)

@socketio.on("leave", namespace='/')
def leave(channel,timenow):
    ##==================== Send message to announce that user has left the channel """
    #channel = session.get('current_channel')
    #leave_room(channel)
    username=session.get('username')
    msg=username + ' has left the channel'
    if "msgs" in channelWiseMessages[channel]:
        temp_channelWiseMessages=channelWiseMessages[channel]["msgs"]
        add_msg={(list(temp_channelWiseMessages)[-1])+1: [username,timenow,msg]}
        temp_channelWiseMessages.update(add_msg)
        
        if len(temp_channelWiseMessages)>100:
            temp_channelWiseMessages.pop((list(temp_channelWiseMessages)[-1])-100)

    data={'user': session.get('username'),'timenow': timenow,'msg':msg }
    emit('status', data, channel=channel,broadcast=True)
    session.pop('username', None)
    session.clear()# Delete cookie    
    return redirect("/")
    
@socketio.on('send')
def send(msg,timenow,channel):
    #channel=session.get('current_channel')
    username=session.get('username')

    #username=session['username']
    #channel=session['current_channel']
    print(f"================user=={username}")
    print(f"=============channel=={channel}")
    
    #username=session.get('username')
    
    if "msgs" in channelWiseMessages[channel]:
        temp_channelWiseMessages=channelWiseMessages[channel]["msgs"]

        add_msg={(list(temp_channelWiseMessages)[-1])+1: [username,timenow,msg]}
        temp_channelWiseMessages.update(add_msg)
        
        if len(temp_channelWiseMessages)>100:
            temp_channelWiseMessages.pop((list(temp_channelWiseMessages)[-1])-100)

    print(f"=============all messages=={channelWiseMessages[channel]}")
        
    data={'user': session.get('username'),'timenow': timenow,'msg': msg}
    emit("announce", data, broadcast=True)
    