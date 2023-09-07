import React from 'react'

const OutputBox = ({payload}) => {
    const {translation, pronunciation, ...rest} = payload

    return (
        <div className='card'>
            <h3>{translation}</h3>
            <p>{pronunciation}</p>
        </div>
    )
}

export default OutputBox
