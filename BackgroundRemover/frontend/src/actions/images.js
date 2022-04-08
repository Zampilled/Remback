import axios from "axios";
import {GET_IMAGE} from "./types";


//GET_IMAGE
export const getImage = (image) => dispatch =>{
    axios.post('/api/', image)
        .then(res =>{
            dispatch({
                type: GET_IMAGE,
                payload: res.data
            })
            console.log('getImage')
        }).catch(err=>console.log(err))
}

