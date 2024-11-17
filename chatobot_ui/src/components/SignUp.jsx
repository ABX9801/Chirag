import axios from 'axios';
import React from 'react'
import { useState } from 'react';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';


const SignUp = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");  
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");

    const onSubmit = async () => {
        try{
            const response = await axios.post(
                "http://localhost:8000/api/user/create",
                {
                    user_create : {
                        username : username,
                        password : password,
                        email : email
                    }
                }
            )
            if (response.data.username === "ERROR") {
                throw new Error("Error in Creating User. Please try again")
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
        SIGN UP FORM
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
        <button type="button" onClick={onSubmit}>SignUp</button>
    </form>    
  )
}

export default SignUp;