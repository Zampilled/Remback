import React,{Component, Fragment} from "react";
import ReactDOM from "react-dom"
import Upload from "./upload/Upload";

import {Provider} from "react-redux";
import store from "../store";

class App extends Component{
    render() {
        return(
            <Provider store={store}>
                <Upload/>
            </Provider>
        )
    }
}
ReactDOM.render(<App /> , document.getElementById('app'))