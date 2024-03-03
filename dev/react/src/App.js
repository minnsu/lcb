import React, {useState} from 'react';
import ReactDOM from 'react-dom/client';

import './App.css';
import {ReactComponent as EnterSVG} from './enter.svg';
import {ReactComponent as SettingSVG} from './setting.svg';
import {ReactComponent as AdjustSVG} from './adjust.svg';
import $ from 'jquery';

function Left(props) {
  return (
    <div className="Left">
      <h2>The Chat</h2>
      <SettingSVG className="SettingSVG" onClick={function () {
        $(".SettingPopupPage").show();
      }}></SettingSVG>
      <SettingPopupPage></SettingPopupPage>
      <hr></hr>
      <div id="ChatListWrapper">
        <ChatList titles={["Chat_1", "Chat_2", "Chat_3"]}></ChatList>
      </div>

      <b>Title</b> <input id="NewChatTitle" type="text"></input>
      <button id="AddNewChat" onClick={function() {
        let newchat = {
          title: document.getElementById("NewChatTitle").value
        }
        fetch("http://localhost:8000/api/newchat", {
          method: "POST",
          headers: {"Content-type": "application/json"},
          body: JSON.stringify(newchat)
        })
        .then(response => response.json())
        .then(result => {
          console.log(result);
          let messages = document.getElementsByClassName("Message");
          while(messages.length) {
            messages[0].remove();
          }
        })
      }}>Add new chat</button>
    </div>
  )
}

function SettingPopupPage(props) {
  return (
    <div className="SettingPopupPage">
      <b id="SettingPopupPage_Title">Setting</b>
      <form className="SettingForm">
        <b>Storage path </b><input id="storage_path" type="text"></input><hr/>
        <b>Model path </b><input id="model_path" type="text"></input><hr/>
        <b>Model Parameters </b><br/>
        [ Temperature ]<br/>
        0 <input id="temperature" type="range" min="0" max="1" step="0.01"></input> 1 <br/>
        [ Top p ]<br/>
        0 <input id="top_p" type="range" min="0" max="1" step="0.01"></input> 1 <br/>
        [ Repetition penalty ]<br/>
        1 <input id="repetition_penalty" type="range" min="1" max="2" step="0.01"></input> 2<br/>
        [ Max new tokens ]<br/>
        2^5 <input id="max_new_tokens" type="range" min="5" max="12" step="1"></input> 2^12<br/>
      </form>

      <div className="SettingPopupPage_Buttons">
        <button id="SettingForm_Apply" onClick={function() {
          let setting_input = {};
          document.querySelectorAll(".SettingForm input").forEach(
            (e) => {
              if(parseFloat(e.value))
                setting_input[e.id] = parseFloat(e.value);
              else
                setting_input[e.id] = e.value;
            }
          );
          fetch("http://localhost:8000/api/setting", {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(setting_input)
          })
          .then(response => response.json())
          .then(result => {
            let chatlistwrapper = document.getElementById("ChatListWrapper");
            chatlistwrapper.removeChild(chatlistwrapper.firstChild);
            
            let root = ReactDOM.createRoot(chatlistwrapper);
            root.render(<ChatList titles={result.titles}/>);
          });
        }}>Apply</button>
        <button id="SettingPopupPage_Close" onClick={function() {
          $(".SettingPopupPage").hide();
        }}>Close</button>
      </div>
    </div>
  )
}

function ChatList(props) {
  return (
    <div id="ChatList">
      {props.titles.map((_title, idx) =>(
        <ChatListItem title={_title}></ChatListItem>
      ))}
    </div>
  )
}

function ChatListItem(props) {
  return (
    <p className="ChatListItem" onClick={function () {
      fetch("http://localhost:8000/api/messages?title=" + props.title)
      .then(response => response.json())
      .then(result => {
        console.log(result);
        let messages = document.getElementsByClassName("Message");
        while(messages.length) {
          messages[0].remove();
        }
      })
    }}>
      {props.title}
    </p>
  )
}

function Right(props) {
  return (
    <div className="Right">
      <div className="MessageArea">
        <Message mid="1" message="Message 1"></Message>
        <Message mid="2" message="Message 2"></Message>
        <Message mid="3" message="Message 3"></Message>
        <Message mid="4" message="Message 4"></Message>
      </div>
      <Input></Input>
    </div>
  )
}

function Message(props) {
  let color = "#FFFFFF";
  if(Number(props.mid) % 2 === 0)
    color = "#DDDDDD";

  return (
    <div className="Message" style={{backgroundColor: color}}>
      <p>
        {props.message}
      </p>
    </div>
  )
}

function Input(props) {
  return (
    <div className="Input">
      <OptionPopupPage></OptionPopupPage>
      <form className="InputForm">
        <AdjustSVG id="InputForm_Option" onClick={function() {
          $(".OptionPopupPage").show();
        }}>+</AdjustSVG>
        <textarea id="InputForm_Text"></textarea>
        <EnterSVG id="InputForm_Send" onClick={function() {
          let input_dom = document.getElementById("InputForm_Text");
          let input_message = {
            text: input_dom.value
          };
          fetch("http://localhost:8000/api/input", {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(input_message)
          })
          .then(response => response.json())
          .then(result => {
            console.log(result);
            // Receive and add to main area messages
          });
          input_dom.value = "";
        }}>Send</EnterSVG>
      </form>
    </div>
  )
}

function OptionPopupPage(props) {
  return (
    <div className="OptionPopupPage">
      <div className="OptionPopupPage_Buttons">
        <button id="OptionPopupPage_Close" onClick={function() {
          let option_input = {
            search: "disabled",
            file_path: document.getElementById("filepath").value,
            text_context: document.getElementById("text_context").value
          };
          
          fetch("http://localhost:8000/api/option", {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(option_input)
          })
          .then(response => response.json())
          .then(result => {
            console.log(result);
          });

          $(".OptionPopupPage").hide();
        }}>Close</button>
      </div>
      <form className="OptionForm">
        <b>Search</b><input id="search" type="checkbox" disabled></input> - Currently Disabled -
        <hr></hr>
        <b>PDF/TXT file path </b><input id="filepath" type="text"></input>
        <hr></hr>
        <b>Context</b>
        <br></br>
        <textarea id="text_context" rows="14" cols="64"></textarea>
      </form>
    </div>
  )
}

function App() {
  return (
    <div className="App">
      <Left></Left>
      <Right></Right>
    </div>
  );
}

export default App;
