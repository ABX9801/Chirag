import React, { useEffect } from "react";
import axios from 'axios';
import Chatbot from 'react-chatbotify';
import Cookies from 'js-cookie';
import { useNavigate } from "react-router-dom";

export const Aaradhya = () => {
  const navigate = useNavigate();
  const [hasError, setHasError] = React.useState(false);

  useEffect(() => {
    const username = Cookies.get("USER_TOKEN");
    if (!username) {
      navigate("/login");
    }
  }, []);

  const chatWithAradhya = async (params) => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/chat",
        {
          chat_input: params.userInput,
        },
        {
          headers: {
            Authorization:
              "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN0cmluZyIsInBhc3N3b3JkIjoic3RyaW5nIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIn0.aKRJmsIeTQFxSYsYzADY4XgxG1sK3xD6376NW4n_5R4",
          },
        }
      );
      console.log(response);
      await params.injectMessage(response.data.response);
    } catch (error) {
      setHasError(true);
      await params.injectMessage(
        "There seems to be a problem with me. Please try again after sometime"
      );
    }
  };

  const flow = {
    start: {
      message: "Hello My name is Aradhya, I am here to help you",
      path: "loop",
    },
    loop: {
      message: async (params) => {
        await chatWithAradhya(params);
      },
      path: () => {
        if (hasError) {
          return "start";
        }
        return "loop";
      },
    },
  };
  return <Chatbot flow={flow} />;
};
