import React, { useState } from 'react'
import InputBox from './inputs'
import OutputBox from './outputs'

const API_URL = '';

const Search = ({ csrftoken, userID }) => {
    const [search, setSearch] = useState("")
    const [data, setData] = useState("")

    console.log("SEARCH", csrftoken)

    const handleSearch = () => {
        // Simulate an API call to Django Backend
        fetch(`/api/translate/`, {
            credentials: 'include',
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
                <InputBox csrftoken={csrftoken} handleInputChange={setSearch}/>
                <OutputBox csrftoken={csrftoken} payload={data}/>
            </div>
            <button onClick={handleSearch}>Search</button>
        </div>
    )
}

export default Search
