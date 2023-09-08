const API_URL = process.env.REACT_APP_API_URL;


class Queries {
    constructor(csrftoken) {
        this.csrftoken = csrftoken
    }

    async removeUserQuery(queryID) {
        console.log('queryID', queryID, `${API_URL}/api/remove_query/${queryID}`)
        return fetch(`${API_URL}/api/remove_query/${queryID}`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrftoken,
            },
            body: {},
        })
        .then(response => response.json())
    }
    
    async getUserQuery(userID) {
        return fetch(`${API_URL}/api/get_queries/${userID}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrftoken,
            },
            // body: JSON.stringify({ query: search }),
        })
        .then(response => response.json())
    }
}


export default Queries