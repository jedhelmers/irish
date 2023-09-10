import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Search from './search';  // Change paths as per your directory structure
import FlashcardsComponent from './flashcards';

function Main({ csrftoken, userID }) {
    return (
        <main>
            <Routes>
                <Route path="/flashcards" element={<FlashcardsComponent csrftoken={csrftoken} userID={userID}/>} />
                <Route path="/search" element={<Search csrftoken={csrftoken} userID={userID}/>} />
            </Routes>

        </main>
    );
}

export default Main;
