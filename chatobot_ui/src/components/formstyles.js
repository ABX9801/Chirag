import styled from 'styled-components';

export const FormContainer = styled.div`
    display : flex; 
    flex-direction : column;
    justify-content : center;
    align-items : center;
    border:1px solid black;
    width : 40%;
    padding : 1%;
    height : 70%;
    margin-top : 5%;
    border-radius : 8px;
    box-shadow: 10px 10px grey;
` 

export const TextInput = styled.input`
    width : 100%;
    border-radius :  4px;
    height : 20px;
    margin : 1%;
`

export const FormTitle = styled.div`
    font-family : Courier, monospace;
`

export const LoginButton = styled.button`
    width : 20%;
    border-radius :  4px;
    height : 30px;
    margin : 1%;
    cursor : pointer;
    &:hover {
        background-color : grey;
    }

`