import React, { useState, useEffect } from 'react';
import Queries from '../utils'

const API_URL = process.env.REACT_APP_API_URL;


function FlashcardsComponent({ csrftoken }) {
    const [activeCard, setActiveCard] = useState(0);
    const [isFlipped, setIsFlipped] = useState(false);
    const [flashcards, setFlashcards] = useState([]);
    const [selectedTag, setSelectedTag] = useState("");  // For the currently selected tag from the combobox
    const [selectedTags, setSelectedTags] = useState({});
    const [tags, setTags] = useState([]);
    const [showEnglish, setShowEnglish] = useState(true);
    const [userGuess, setUserGuess] = useState("");
    const queries = new Queries(csrftoken)

    const user_id = 4;  // This can be dynamic based on your app's requirements
    
    const removeQuery = async (queryID) => {
        queries.removeUserQuery(queryID)
        .then(console.log)
    }

    const handleAddTag = (query_id) => {
        if (selectedTag) {
            fetch(`${API_URL}/api/add_tags/${query_id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ tags: [selectedTag] })  // Sending as a list
            })
            .then(response => response.json())
            .then(data => {
                // Assuming your API returns the updated tags for the query after adding
                const updatedFlashcards = [...flashcards];
                updatedFlashcards[activeCard].tags = data.tags;
                setFlashcards(updatedFlashcards);
            })
            .catch(error => {
                console.error('Error adding the tag:', error);
            });
        }
    };
    
    const handleRemoveTag = (tagToRemove, query_id) => {
        // You'd probably have a DELETE or a similar endpoint for this. Adjust accordingly.
        fetch(`${API_URL}/api/remove_tag/${query_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tags: [tagToRemove] })  // Sending as a list
        })
        .then(response => response.json())
        .then(data => {
            const updatedFlashcards = [...flashcards];
            updatedFlashcards[activeCard].tags = data.tags;
            setFlashcards(updatedFlashcards);
        })
        .catch(error => {
            console.error('Error removing the tag:', error);
        });
    };

    const submitGuess = (cardId) => {
        fetch(`${API_URL}/api/submit_guess/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ guess: userGuess, query_id: cardId })
        })
        .then(response => response.json())
        .then(data => {
            if(data.isCorrect) {
                alert("Correct guess!");
            } else {
                alert("Incorrect guess!");
            }
        })
        .catch(error => {
            console.error('Error submitting the guess:', error);
        });
    };
    
    useEffect(() => {
        // Fetch data based on selected tags
        console.log(Object.keys(selectedTags).filter(tag => selectedTags[tag]))
        fetch(`${API_URL}/api/get_queries/${user_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ tags: Object.keys(selectedTags).filter(tag => selectedTags[tag]) })
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                setFlashcards(data);
            })
            .catch(error => {
                console.error('There was an error fetching the flashcards:', error);
            });
    }, [selectedTags]);  

    const toggleTag = (tag) => {
        setSelectedTags(prevState => ({
            ...prevState,
            [tag]: !prevState[tag]
        }));
    };

    const clearTags = () => {
        setSelectedTags({});
    };

    useEffect(() => {
        fetch(`${API_URL}/api/get_queries/${user_id}/`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                setFlashcards(data);
            })
            .catch(error => {
                console.error('There was an error fetching the flashcards:', error);
            });
    }, []);

    useEffect(() => {
        async function fetchTags() {
            try {
                const response = await fetch(`${API_URL}/api/tags/`);
                if (!response.ok) {
                    console.error("Failed to fetch tags");
                    return;
                }
                const tagsData = await response.json();
                setTags(tagsData);
                console.log(tagsData)
            } catch (error) {
                console.error("Error fetching tags:", error);
            }
        }

        fetchTags();
    }, []);

    const toggleFlip = () => {
        setIsFlipped(!isFlipped);
    };

    const nextCard = () => {
        if (activeCard < flashcards.length - 1) {
            setActiveCard(activeCard + 1);
            setIsFlipped(false);  // Reset flip for the new card
        }
    };

    const prevCard = () => {
        if (activeCard > 0) {
            setActiveCard(activeCard - 1);
            setIsFlipped(false);  // Reset flip for the new card
        }
    };

    return (
        <div className="flashcard-wrapper">
            <div className="tag-container">
                {tags.map(tag => (
                    <label key={tag}>
                        <input 
                            type="checkbox" 
                            checked={!!selectedTags[tag]} 
                            onChange={() => toggleTag(tag)}
                        />
                        {tag}
                    </label>
                ))}
                <button onClick={clearTags}>Clear</button>
            </div>

            <div>
                <h2>Flashcards</h2>

                <div className="card-display">
                    {showEnglish ? flashcards[activeCard]?.english : flashcards[activeCard]?.irish}
                </div>

                <div className="guess-section">
                    <input type="text" value={userGuess} onChange={(e) => setUserGuess(e.target.value)} placeholder="Your guess..." />
                    <button onClick={() => submitGuess(flashcards[activeCard].id)}>Submit Guess</button>
                </div>

                <button onClick={() => setShowEnglish(!showEnglish)}>Toggle Language</button>

                <div style={{ display: 'flex', justifyContent: 'flex-end', marginRight: 100, padding: 10 }}>
                    <div>
                        Delete 
                        <i className="fas fa-trash trash fa-sm" onClick={() => removeQuery(flashcards[activeCard].id)}></i>
                    </div>
                </div>
                <div style={{ display: "flex" }}>
                    
                    <button className='card-button' onClick={prevCard} disabled={activeCard === 0}>Previous</button>
                    {
                        !!flashcards[activeCard] && (
                            <div className="flashcard-container" onClick={toggleFlip}>
                                {isFlipped ? 
                                    flashcards[activeCard].input_text : 
                                    activeCard && flashcards[activeCard]?.output_text &&
                                        <>
                                            <div>{flashcards[activeCard].output_text}</div>
                                            <div className="pronunciation">{flashcards[activeCard].pronunciation}</div>
                                        </>
                                    
                                }
                            </div>
                        )
                    }
                    <button className='card-button' onClick={nextCard} disabled={activeCard === flashcards.length - 1}>Next</button>
                </div>

                <h2>Filter</h2>
                <div className="tag-management">
                    <div className="tag-add-container">
                        <select value={selectedTag} onChange={(e) => setSelectedTag(e.target.value)}>
                            <option value="">--Select a tag--</option>
                            {tags.map(tag => <option key={tag} value={tag}>{tag}</option>)}
                        </select>
                        <i className="fas fa-plus-circle" onClick={() => handleAddTag(flashcards[activeCard].id)}></i>  {/* Assuming flashcards have an "id" property */}
                    </div>

                    <div className="tags-display">
                        {flashcards[activeCard]?.tags?.map(tag => (
                            <span key={tag} className="tag">
                                {tag}
                                <i className="fas fa-times" onClick={() => handleRemoveTag(tag, flashcards[activeCard].id)}></i>
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default FlashcardsComponent;
