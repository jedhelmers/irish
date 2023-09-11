const API_URL = '';


class Queries {
    constructor(csrftoken) {
        this.csrftoken = csrftoken
    }

    async removeUserQuery(queryID) {
        console.log('queryID', queryID, `/api/remove_query/${queryID}`)
        return fetch(`/api/remove_query/${queryID}`, {
            credentials: 'include',
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
        return fetch(`/api/get_queries/${userID}`, {
            credentials: 'include',
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