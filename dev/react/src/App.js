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
        <b>Storage path </b><input type="text"></input>
        <hr></hr>
        <b>Model path </b><input type="text"></input>
        <hr></hr>
        <b>Model Parameters </b>
        <br></br>
        [ Temperature ]
        <br></br>
        0 <input name="temperature" type="range" min="0" max="1" step="0.01"></input> 1
        
        <br></br>
        [ Top p ]
        <br></br>
        0 <input name="top_p" type="range" min="0" max="1" step="0.01"></input> 1
        
        <br></br>
        [ Repetition penalty ]
        <br></br>
        1 <input name="repetition_penalty" type="range" min="1" max="2" step="0.01"></input> 2
        
        <br></br>
        [ Max tokens ]
        <br></br>
        2^5 <input name="max_tokens" type="range" min="5" max="12" step="1"></input> 2^12
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
        <b>Search</b><input type="checkbox" value="Search" disabled></input> - Currently Disabled -
        <hr></hr>
        <b>Select PDF/TXT file </b><input type="file"></input>
        <hr></hr>
        <b>Context</b>
        <br></br>
        <textarea rows="14" cols="64"></textarea>
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
