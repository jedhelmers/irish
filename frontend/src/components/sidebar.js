import React from 'react';
import { Link } from 'react-router-dom';


function Sidebar() {
    return (
        <div className="sidebar">
            <ul className="sidebar-menu">
                <li><Link to="/search">Search</Link></li>
                <li><Link to="/flashcards">Review as Flashcards</Link></li>
                <a href="http://localhost:3001">Grafana</a>

            </ul>
        </div>
    );
}

export default Sidebar;