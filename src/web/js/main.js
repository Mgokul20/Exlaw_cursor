// const connection = require ("./index");
// var mysql = require('mysql');
// import {mysql} from "mysql";
// var mysql = require('mysql');
// var con = mysql.createConnection({
//     host: "localhost",
//     user: "root",
//     password: "",
//     database: "test"
//   });
//user clicked button
document.getElementById("userInputButton").addEventListener("click", getUserInput, false);
//user pressed enter '13'
document.getElementById("userInput").addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        //cancel the default action
        event.preventDefault();
        //process event
        getUserInput();
    }
});

eel.expose(addUserMsg);
eel.expose(addAppMsg);
async function pass_message(msg){
  console.log("calling done");
  const rawResponse = await fetch('https://localhost/post', {
    method: 'POST',
    mode:'no-cors',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: {"Message":`${msg}`}
  })
  console.log(rawResponse);
  return rawResponse;

}

function addUserMsg(msg) {
    
    element = document.getElementById("messages");
    element.innerHTML += '<div class="message from ready rtol">' + msg + '</div>';
    element.scrollTop = element.scrollHeight - element.clientHeight - 15;
    //add delay for animation to complete and then modify class to => "message from"
    index = element.childElementCount - 1;
    (async () => {
        const rawResponse = await fetch('https://localhost/post', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: {"Message":`${msg}`}
        });
        const content = await rawResponse.json();
      
        console.log(content);
      })();
    setTimeout(changeClass.bind(null, element, index, "message from"), 500);
    
    // con.connect(function(err) {
    // con.query(`INSERT INTO exlaw(type,message) values (user,${msg})`, function (err, result) {
    //     if (err) throw err;
    //     console.log("DATA created");
    //   });});
}

function addAppMsg(msg) {
    
    element = document.getElementById("messages");
    element.innerHTML += '<div class="message to ready ltor">' + msg + '</div>';
    element.scrollTop = element.scrollHeight - element.clientHeight - 15;
    //add delay for animation to complete and then modify class to => "message to"
    index = element.childElementCount - 1;
    (async () => {
        const rawResponse = await fetch('https://localhost/post', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: {"Message":`${msg}`}
        });
        const content = await rawResponse.json();
      
        console.log(content);
      })();
    setTimeout(changeClass.bind(null, element, index, "message to"), 500);
    
    //  var sql = `INSERT INTO exlaw(type,message) values (app,${msg})`;
    // con.connect(function(err) {
    // con.query(`INSERT INTO exlaw(type,message) values (app,${msg})`, function (err, result) {
    //     if (err) throw err;
    //     console.log("Table created");
    //   });
    // });
};

function changeClass(element, index, newClass) {
    console.log(newClass +' '+ index);
    element.children[index].className = newClass;
}

function getUserInput() {
    element = document.getElementById("userInput");
    msg = element.value;
    if (msg.length != 0) {
        element.value = "";
        eel.getUserInput(msg);
    }
}