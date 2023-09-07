import React, { useState } from 'react'
import InputBox from './inputs'
import OutputBox from './outputs'

const API_URL = process.env.REACT_APP_API_URL;

console.log('API_URL', API_URL)
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
                setData(data.translation);
            } else {
                console.error("Nope. Translation failed.")
                // handle error here
            }
        });
    }

    return (
        <div>
            <InputBox handleInputChange={setSearch}/>
            <OutputBox text={data}/>
            <button onClick={handleSearch}>Search</button>
        </div>
    )
}

export default Main
