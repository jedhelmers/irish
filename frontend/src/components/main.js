import React, { useState } from 'react'
import InputBox from './inputs'
import OutputBox from './outputs'

const API_URL = process.env.REACT_APP_API_URL;

const Main = ({ csrftoken }) => {
    const [search, setSearch] = useState("")
    const [data, setData] = useState("")

    const handleSearch = () => {
        // Simulate an API call to Django Backend
        fetch(`${API_URL}/api/translate/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ query: search }),
        })
        .then(response => response.json())
        .then(data => {
            data = JSON.parse(data.task)
            console.log(data)
            if (data.err === null) {
                setData(data);
            } else {
                console.error("Nope. Translation failed.")
                // handle error here
            }
        });
    }

    return (
        <div>
            <div className='main'>
                <InputBox handleInputChange={setSearch}/>
                <OutputBox payload={data}/>
            </div>
            <button onClick={handleSearch}>Search</button>
        </div>
    )
}

export default Main
