import React, { useState } from 'react'
import InputBox from './inputs'
import OutputBox from './outputs'

const Main = ({ csrftoken }) => {
    const [search, setSearch] = useState("")
    const [data, setData] = useState("")

    const handleSearch = () => {
        // Simulate an API call to Django Backend
        fetch('/api/translate/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ query: search }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data?.translation) {
                console.log('data.result', data.result)
                if (data.translation.err === null) {
                    setData(data.translation.result);
                } else {
                    console.error("Nope. Translation failed.")
                    // handle error here
                }
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
