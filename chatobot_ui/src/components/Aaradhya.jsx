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
    const user_token = Cookies.get("USER_TOKEN");
    try {
      const response = await axios.post(
        "http://localhost:8000/api/chat",
        {
          chat_input: params.userInput,
        },
        {
          headers: {
            Authorization:
              `Bearer ${user_token}`,
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
