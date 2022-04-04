import React, {Component} from 'react';
import {connect} from "react-redux";
import PropTypes from 'prop-types';
import {getImage} from "../../actions/images";
import mapStateToProps from "react-redux/lib/connect/mapStateToProps";


class Upload extends Component {
    state ={
        img: '',
        imgUrl: ''
    }
    static propTypes = {
        image: PropTypes.array.isRequired,
        getImage: PropTypes.func.isRequired,
    }
    onImage = e => {
        let file = e.target.files[0]
        this.setState({img: file})
        this.setState({[e.target.name]: e.target.value})
        this.setState({'imgUrl':URL.createObjectURL(e.target.files[0])})
        console.log(this.state)

    }
    onSubmit = e =>{
        e.preventDefault()
        let formdata = new FormData()
        formdata.append('image', this.state.img)
        this.props.getImage(formdata)
        this.setState({
            img: '',
            imgUrl: ''
        })
    }
    render() {
        const{img} = this.state.img
        return (
            <div className="">
                <form onSubmit={this.onSubmit}>
                <div className="col-md-4 card m-auto shadow car border-danger mt-4">
                    <div className="card-header text-center ">
                        <h2>Background Remover</h2>
                    </div>
                    <div className="card-body text-center">
                        <div className="container-lg text-center media-middle card card-body border-warning d-flex align-content-center" >
                            {this.props.image?<img className="rounded shadow " src={this.props.image}></img>: this.state.img?<img className="rounded shadow " src={this.state.imgUrl}></img>: <label className="label">No Image Uploaded</label>}
                        </div>

                                <input
                                    id="image-control"
                                    className="form-control"
                                    type="file"
                                    accept="image/*"
                                    name="image"
                                    onChange={this.onImage}
                                    value={img}
                                />
                    </div>
                    <div className="card-footer text-center">

                            <button type="submit" className="btn btn-warning btn-lg"  >{' '}Remove Background</button>

                    </div>

                </div>
                </form>
            </div>

        );
    }
}
const mapStatetoProps = state =>({
    image: state.images.image
})

export default connect(mapStatetoProps, {getImage})(Upload);