document.addEventListener('DOMContentLoaded', () => 
{
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);    
socket.on('connect', () => 
  {
/* 
    document.querySelector('#leave_channel').addEventListener('click', () => 
  {
        //socket.emit('leave');                      // Notify the server user has disconnected
        localStorage.removeItem('last_channel');      //remove channel from local storage
        //window.location.replace('/');             //relocate window location
  });
  
  document.querySelector('#user_logout_btn').addEventListener('click', () => 
  {
        //socket.emit('leave');                      // Notify the server user has disconnected
        localStorage.removeItem('last_channel');      //remove channel from local storage
        localStorage.removeItem('username');      //remove channel from local storage
        //window.location.replace('/');             //relocate window location
  });
*/
  

/*  document.getElementById("logout").onclick = function() {myFunction()};

    function myFunction() 
    {       
      
      let timenow = new Date;
      timenow = timenow.toLocaleTimeString();
      last_channel=localStorage.getItem('last_channel')
      event.preventDefault();
      localStorage.removeItem('last_channel');
      localStorage.removeItem('username')
      
      location.reload();
      socket.emit('leave',last_channel,timenow);
    }  

      document.querySelector('#logout').addEventListener('click', () => 
          {
            event.preventDefault();
            let timenow = new Date;
            timenow = timenow.toLocaleTimeString();
            channel=localStorage.getItem('last_channel');
            socket.emit('leave',channel,timenow);
            
            localStorage.removeItem('last_channel');
            localStorage.removeItem('username', data.user)

          });
*/      document.querySelector("#send_msg").addEventListener("click",() => 
          {
          event.preventDefault();
          //const msg=document.querySelector('#my_msg').value;
          let temp_msg=document.querySelector('#my_msg').value;
          
          
          const msg=temp_msg.replace("\n", "");

          
          document.querySelector('#my_msg').value;
          channel=localStorage.getItem('last_channel');
          let timenow = new Date;
          timenow = timenow.toLocaleTimeString();
          socket.emit('send', msg,timenow,channel);
          

          document.getElementById('my_msg').focus();
          document.getElementById('my_msg').value=null;

          document.querySelector('#my_msg').value = "";    // Clear input field and disable button again\
          
          });//===5
    });  
  
  socket.on('announce', data => 
  {
    
    const new_msg=`${data.msg} - ${data.user}(${data.timenow})`    
    const msg_div = document.createElement('div');
    msg_div.innerHTML = new_msg;

    msg_div.setAttribute("class",'alert alert-dark');   
    msg_div.setAttribute("style","width:50%; height:auto; margin-left:1%; margin-right:50%;");
    if (my_username === data.user) 
    {
      msg_div.setAttribute("style","width:50%; height:auto; margin-left:50%; margin-right:0%;");
      msg_div.setAttribute("class",'alert alert-success');
    } 
    msg_div.setAttribute("role","alert");
    
    
    document.querySelector('#all_messages').appendChild(msg_div);
    
    var myDiv = document.getElementById("all_messages");
    myDiv.scrollTop = myDiv.scrollHeight;

  });

  socket.on('status', data => 
  {
    const new_msg=`${data.msg} -(${data.timenow})`    
    const msg_div = document.createElement('div');
    msg_div.innerHTML = new_msg;

    msg_div.setAttribute("class",'alert alert-dark');   
    msg_div.setAttribute("style","width:50%; height:auto; margin-left:1%; margin-right:50%;");
    if (my_username === data.user) 
    {
      msg_div.setAttribute("style","width:50%; height:auto; margin-left:50%; margin-right:0%;");
      msg_div.setAttribute("class",'alert alert-success');
    } 
    msg_div.setAttribute("role","alert");
    document.querySelector('#all_messages').appendChild(msg_div);
    var myDiv = document.getElementById("all_messages");
    myDiv.scrollTop = myDiv.scrollHeight;
    //localStorage.setItem('last_channel', data.channel)
    //localStorage.setItem('username', data.user)
  });
  
    
});

