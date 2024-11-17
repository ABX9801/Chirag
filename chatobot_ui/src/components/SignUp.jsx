import axios from 'axios';
import React from 'react'
import { useState } from 'react';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import { FormContainer, TextInput, FormTitle, LoginButton } from './formstyles';


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
    <center>
    <FormContainer>
        <FormTitle>SIGN UP FORM</FormTitle>
        <br />
        <label>
            <TextInput type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder='Username' />
        </label>
        <br />
        <label>
            <TextInput type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder='Password'/>
        </label>
        <br />
        <label>
            <TextInput type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder='Email'/>
        </label>
        <br />
        <LoginButton type="button" onClick={onSubmit}>SignUp</LoginButton>
    </FormContainer>    
    </center>
  )
}

export default SignUp;