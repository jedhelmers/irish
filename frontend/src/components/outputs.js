import React from 'react'


const OutputBox = ({csrftoken, payload}) => {
    const {translation, pronunciation, queryID, ...rest} = payload

    return (
        <div className='card'>
            <div className='textbody'>
                <h3>{translation}</h3>
                <p>{pronunciation}</p>
            </div>
        </div>
    )
}

export default OutputBox
