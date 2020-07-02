document.addEventListener('DOMContentLoaded', () => 
{//====0

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);    
  
  socket.on('connect', () => 
      {//=====0----1

      //==========================on click send message button ========================
      //document.querySelector('#new_msg').onsubmit = () => 
      document.querySelector("#new_msg").addEventListener("click",() => 
      {//====5
        
        const msg=document.querySelector('#my_msg').value;
        alert(`RECEIVED MESSAGE IN INDEX.JS ${msg}`)  //****************************
        let timenow = new Date;
        timenow = timenow.toLocaleTimeString();
        
        socket.emit('submit msg', msg,timenow);
        document.querySelector('#my_msg').value = '';    // Clear input field and disable button again\
        
        //document.querySelector('#send_msg').disabled = true;
        //return false;
      });//===5
  
//====================== When user joins a channel, add a message and on users connected.
socket.on('status', data => 
{//=====6
  

  //========== Broadcast message of joined user.
  
  let row = '<' + `${data.msg}` + '>'
  document.querySelector('#all_messages').value += row + '\n';
  
  //==============================
    div = document.createElement('div');
    div.innerHTML = `${data.msg}`;
    let myStyle = ['alert alert-primary', 'alert alert-success', 'alert alert-danger', 'alert alert-warning', 'alert alert-info', 'alert alert-light', 'alert alert-dark'];
    let mySelectedStyle = myStyle[Math.floor(Math.random() * myStyle.length)];
    alert(mySelectedStyle)
    div.setAttribute("class",mySelectedStyle);
    div.setAttribute("role","alert");
    div.setAttribute("style","width:50%; height:auto; margin-left:1%; margin-right:50%;");

    let row = '<' + `${data.timenow}` + '> - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`
    document.querySelector('#all_messages').value += row + '\n'
    //=====================
    // Save user current channel on localStorage
    localStorage.setItem('last_channel', data.channel)
})//==6

  
  // When a new vote is announced, add to the unordered list
socket.on("announce", data => 
  {//===7

    //alert("i am received data...thank you")
    //alert(`received value ${data.msg}`)//const
    
    div = document.createElement('div');
    div.innerHTML = `${data.msg}`;
    let myStyle = ['alert alert-primary', 'alert alert-success', 'alert alert-danger', 'alert alert-warning', 'alert alert-info', 'alert alert-light', 'alert alert-dark'];
    let mySelectedStyle = myStyle[Math.floor(Math.random() * myStyle.length)];
    alert(mySelectedStyle)
    div.setAttribute("class",mySelectedStyle);
    div.setAttribute("role","alert");
    div.setAttribute("style","width:50%; height:auto; margin-left:1%; margin-right:50%;");

    let row = '<' + `${data.timenow}` + '> - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`
    document.querySelector('#all_messages').value += row + '\n'

    //document.querySelector('#all_messages').appendChild(div);
  });//==7
  
  });//=====0------1

});//====0

