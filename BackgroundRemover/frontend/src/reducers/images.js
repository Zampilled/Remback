import {GET_IMAGE} from '../actions/types.js'

const initialState = {
    image: ''
}

export default function (state=initialState, action){
    switch (action.type){
        case GET_IMAGE:
            return{
                image: action.payload.image
            }
        default:
            return state;
    }
}
