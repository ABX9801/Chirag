import React from 'react'
import Cookies from 'js-cookie'
import styled from 'styled-components'
import { useNavigate } from 'react-router-dom'

const StyledNavBar = styled.div`
    display : flex;
    justify-content : space-between;
    padding : 0.5%;
    background-color : black;
`

const AppName = styled.div`
    font-size : 28px;
    font-family : Courier, monospace;
    font-weight : bold;
    color : white;
`

const UserName = styled.div`
    font-size : 28px;
    font-family : Courier, monospace;
    font-weight : bold;
    color : white;
`

const Logout = styled.div`
    font-size : 28px;
    font-family : Courier, monospace;
    font-weight : bold;
    cursor : pointer;
    color : white;

`

const NavBar = () => {
    const username = Cookies.get("USER_NAME");
    const navigate = useNavigate();

    const logoutUser = () => {
        Cookies.remove("USER_TOKEN");
        Cookies.remove("USER_NAME");
        Cookies.remove("USER_EMAIL");
        alert("User Logged Out Successfully");
        navigate("/login");
    }

    return (
        <StyledNavBar>
            <AppName>Aaradhya</AppName>
            <UserName>User : {username}</UserName>
            <Logout onClick={logoutUser}>Logout</Logout>
        </StyledNavBar>
    )
}

export default NavBar;
