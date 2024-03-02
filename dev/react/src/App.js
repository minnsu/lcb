import './App.css';
import {ReactComponent as EnterSVG} from './enter.svg';
import {ReactComponent as SettingSVG} from './setting.svg';
import {ReactComponent as AdjustSVG} from './adjust.svg';
import $ from 'jquery';

function Left(props) {
  return (
    <div className="Left">
      <h2>Chat Assistant</h2>
      <SettingSVG className="SettingSVG" onClick={function () {
        $(".SettingPopupPage").show();
      }}></SettingSVG>
      <SettingPopupPage></SettingPopupPage>
      <hr></hr>
      <ChatListItem title='Chat 1'></ChatListItem>
      <ChatListItem title='Chat 2'></ChatListItem>
      <ChatListItem title='Chat 3'></ChatListItem>
    </div>
  )
}

function SettingPopupPage(props) {
  return (
    <div className="SettingPopupPage">
      <b id="SettingPopupPage_Title">Setting</b>
      <form className="SettingForm">
        {/* 
        // Model select
        // Parameter - 
        top_p
        temperature
        repetition_penalty
        max_tokens
        etc.
         */}
      </form>
      <div className="SettingPopupPage_Buttons">
        <button id="SettingForm_Apply" onClick={function() {
          alert("Click Setting Apply");
          // fetch("localhost:8000/api/");
        }}>Apply</button>
        <button id="SettingPopupPage_Close" onClick={function() {
          $(".SettingPopupPage").hide();
        }}>Close</button>
      </div>
    </div>
  )
}

function ChatListItem(props) {
  return (
    <p className="ChatListItem" onClick={function () {
      alert("Click " + props.title);
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
      <form className="InputForm">
        <AdjustSVG id="InputForm_Option" onClick={function() {
          $(".OptionPopupPage").show();
        }}>+</AdjustSVG>
        <OptionPopupPage></OptionPopupPage>
        <input type="text" id="InputForm_Text"></input>
        <EnterSVG id="InputForm_Send" onClick={function() {
          alert("Click Enter!");
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
          $(".OptionPopupPage").hide();
        }}>Close</button>
      </div>
      <form className="OptionForm">
        {/* // URL based
        // PDF file
        // Context */}
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
