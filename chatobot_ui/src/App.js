import './App.css';
import SignUp from './components/SignUp';
import { Aaradhya } from './components/Aaradhya';
import Login  from './components/Login';
import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<SignUp/>} />
        <Route path="/chatbot" element={<Aaradhya/>} />
        <Route path="/login" element={<Login/>} />
      </Routes>
    </Router>
  );
}

export default App;
