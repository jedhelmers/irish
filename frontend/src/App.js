import Main from './components/main.js'
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Sidebar from './components/sidebar.js';

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


function App() {
  return (
    <Router>
      <div className="App">
        <div class="container">
          <div class="header">
            <img src={logo} className="App-logo" alt="logo" />
            <div style={{ marginTop: 10 }}>Translate <code>English into Irish</code></div>
          </div>
          <Sidebar />
          <div class="body">
            <Main csrftoken={csrftoken}/>
          </div>
          <div class="footer">
              Footer Content
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
