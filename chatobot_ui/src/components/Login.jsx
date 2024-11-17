import axios from 'axios';
import React from 'react'
import { useState } from 'react';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");  
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("")

    const onSubmit = async () => {
        try{
            console.log("onSubmit")
            const response = await axios.post(
                "http://localhost:8000/api/user/login",
                {
                    user_create : {
                        username : username,
                        password : password,
                        email : email
                    }
                }
            )
            if (response.data.username === "ERROR") {
                throw new Error("Error in Logging in User. Please try again")
            }
            Cookies.set("USER_TOKEN", response.data.token);
            Cookies.set("USER_NAME", response.data.username);
            Cookies.set("USER_EMAIL", response.data.email);
            navigate("/chatbot");
        } catch( error ) {
            console.log(error)
            setUsername("");
            setPassword("");
            setEmail("");
        }
    }

  return (
    <form>
        LOG IN FORM
        <br />
        <label>
            Username:
            <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
        </label>
        <br />
        <label>
            Password:
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </label>
        <br />
        <label>
            Email:
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
        </label>
        <br />
        <button type="button" onClick={onSubmit}>LogIn</button>
    </form>    
  )
}

export default Login;