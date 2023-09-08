import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Search from './search';  // Change paths as per your directory structure
import FlashcardsComponent from './flashcards';

function Main({ csrftoken }) {
    return (
        <main>
            <Routes>
                <Route path="/search" element={<Search />} />
                <Route path="/flashcards" element={<FlashcardsComponent csrftoken={csrftoken}/>} />
            </Routes>

        </main>
    );
}

export default Main;
