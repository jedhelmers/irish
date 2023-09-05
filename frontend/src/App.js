import Main from './components/main'
import axios from 'axios';
import logo from './logo.svg';
import './App.css';

const data = { user_id: 1, notes: [[1, 0], [0, 1]] };

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');


async function fetchSongs() {
  try {
    // Make a GET request to your Django view
    const response = await axios.get(
      '/api/query_songs/',
      {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
      }
    );

    // Check if the request was successful
    if (response.status === 200) {
      console.log('Request successful. Check your Django server logs for query output.');
    } else {
      console.log(`Server returned error: ${response.status}`);
    }
  } catch (error) {
    console.log('There was a problem with the fetch operation:', error);
  }
}

function App() {

  async function postData() {
    console.log(JSON.stringify(data))
    try {
      const response = await axios.post(`/api/create_song/${data.user_id}/`, JSON.stringify(data), {
        withCredentials: false,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        }
      });
      return response.data;
    } catch (error) {
      console.error('There was an error!', error);
    }
  }

  // Usage example
  const data = { user_id: 1, notes: [[1, 0], [0, 1]] };
  postData(data)
    .then(response => {
      console.log(response);
    });


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <Main csrftoken={csrftoken}/>
        <button onClick={postData}>Howdy</button>
        <button onClick={fetchSongs}>Fetch</button>
      </header>
    </div>
  );
}

export default App;
