import React, { useEffect } from "react";
import axios from 'axios';
import Chatbot from 'react-chatbotify';
import Cookies from 'js-cookie';
import { useNavigate } from "react-router-dom";

const getCalendarCode = () => {
  try {
    const code = window.location.href.split("code=")[1].split("&scope")[0];
    return decodeURIComponent(code);
  } catch (error) {
    console.error("Error extracting calendar code:", error);
    return null;
  }
}

const getCalendarAccessToken = () => {
  let access_token = Cookies.get("CALENDAR_ACCESS_TOKEN");
  const code = getCalendarCode();
  if (!code) {
    return
  }
  const user_token = Cookies.get("USER_TOKEN");
  const response = axios.post(
    "http://localhost:8000/api/user/calendar/access",
    {
      calendar_code : code
    },
    {
      headers: {
        Authorization:
          `Bearer ${user_token}`,
      },
    }
  ).catch((err) => {
    console.log(err);
  });
  access_token = response?.access_token;
  Cookies.set("CALENDAR_ACCESS_TOKEN", access_token);
  return access_token;
}

const getLocation = () => {
  const userLattitude = Cookies.get("USER_LATTITUDE");
  const userLongitude = Cookies.get("USER_LONGITUDE");
  if (userLattitude && userLongitude) {
    return
  }
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;
      Cookies.set("USER_LATTITUDE", latitude);
      Cookies.set("USER_LONGITUDE", longitude);
    });
  }
  else {
    alert("Geolocation is not supported by this browser.");
  }
}

export const Aaradhya = () => {
  const navigate = useNavigate();
  const [hasError, setHasError] = React.useState(false);

  useEffect(() => {
    const username = Cookies.get("USER_TOKEN");
    const access_token = getCalendarAccessToken();
    getLocation();
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
