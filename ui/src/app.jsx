import React, {useState, useEffect, useCallback} from 'react'
import axios from "axios";
import "bulma/css/bulma.min.css";
import {Columns, Box} from "react-bulma-components";
import Header from "./components/Header";
import Body from "./components/Body";


function App() {
    return (
        <>
            <Header />
            <Body />
        </>
    );
}

export default App;
