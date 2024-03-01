import './App.css';
import {ReactComponent as EnterSVG} from './enter.svg';
import {ReactComponent as SettingSVG} from './setting.svg';
import {ReactComponent as AdjustSVG} from './adjust.svg';

function Left(props) {
  return (
    <div className="Left">
      <h2>Title</h2>
      <SettingSVG className="SettingSVG" onClick={function () {
        alert("Click Setting!");
      }}></SettingSVG>
      <hr></hr>
      <ChatListItem title='Chat 1'></ChatListItem>
      <ChatListItem title='Chat 2'></ChatListItem>
      <ChatListItem title='Chat 3'></ChatListItem>
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
          alert("Click Adjust!");
        }}>+</AdjustSVG>
        <input type="text" id="InputForm_Text"></input>
        <EnterSVG id="InputForm_Send" onClick={function() {
          alert("Click Enter!");
        }}>Send</EnterSVG>
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
