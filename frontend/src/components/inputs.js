import React from 'react'

const InputBox = ({ handleInputChange }) => {
    return (
        <textarea placeholder='search!' className='card' type='text' onChange={(e) => handleInputChange(e.target.value)}/>
    )
}

export default InputBox
