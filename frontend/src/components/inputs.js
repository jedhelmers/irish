import React from 'react'

const InputBox = ({ handleInputChange }) => {
    return (
        <input type='text' onChange={(e) => handleInputChange(e.target.value)}/>
    )
}

export default InputBox
