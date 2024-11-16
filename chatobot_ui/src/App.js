import './App.css';
import Chatbot from 'react-chatbotify';
import axios from 'axios';
import React from 'react';



function App() {
  const [hasError ,setHasError] = React.useState(false);

  const chatWithAradhya = async (params) => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/chat", 
        {
          chat_input: params.userInput
        },
        {
          headers: {
            Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN0cmluZyIsInBhc3N3b3JkIjoic3RyaW5nIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIn0.aKRJmsIeTQFxSYsYzADY4XgxG1sK3xD6376NW4n_5R4"
          }
        }
      );
      debugger;
      console.log(response);
      await params.injectMessage(response.data.response);
    }catch (error) {
      setHasError(true);
      await params.injectMessage("There seems to be a problem with me. Please try again after sometime");
    }
    
  }
  
    const flow = {
      "start" : {
        "message" : "Hello My name is Aradhya, I am here to help you",
        "path" : "loop"
      },
      "loop" : {
        "message" : async (params) => {
          await chatWithAradhya(params);
        },
        "path" : () => {
          if (hasError) {
            return "start";
          }
          return "loop";
        }
      }
    }
  return (
    <div className="App">
     <Chatbot settings={{general: {embedded: true}, botBubble : {showAvatar : false} }} flow={flow}/>
    </div>
  );
}

export default App;
