import React, { useEffect, useState } from 'react';

import MovieGrid from '../components/MovieGrid';
import MovieSlider from '../components/MovieSlider';

const Home = ({ user, isloggedIn }) => {
    const [knnMovies, setKnnMovies] = useState([]);
    const [popularMovies, setPopularMovies] = useState([]);
    const [ageMovies, setAgeMovies] = useState([]);
    const [occupationMovies, setOccupationMovies] = useState([]);
    const [userAge, setUserAge] = useState('');
    const [userOccupation, setUserOccupation] = useState('');

    useEffect(() => {
        async function fetchKnnMovies() {
            try {
                const response = await fetch(`http://localhost:8001/v1/movies/recommendations/knn/${user.userId}`);
                const data = await response.json();
                setKnnMovies(data);
            } catch (error) {
                console.error('Error fetching KNN movies:', error);
            }
        }

        if (isloggedIn && user) {
            fetchKnnMovies();
        }
    }, [user, isloggedIn]);

    useEffect(() => {
        async function fetchPopularMovies() {
            try {
                const response = await fetch('http://localhost:8001/v1/movies/most-rated-last-month');
                const data = await response.json();
                setPopularMovies(data);
            } catch (error) {
                console.error('Error fetching popular movies:', error);
            }
        }

        fetchPopularMovies();
    }, []);

    useEffect(() => {
        async function fetchAgeMovies() {
            try {
                const response = await fetch(`http://localhost:8001/v1/movies/age/${user.userId}`);
                const data = await response.json();
                setAgeMovies(data.movies);
                setUserAge(data.user_age);
            } catch (error) {
                console.error('Error fetching age movies:', error);
            }
        }

        if (isloggedIn && user) {
            fetchAgeMovies();
        }
    }, [user, isloggedIn]);

    useEffect(() => {
        async function fetchOccupationMovies() {
            try {
                const response = await fetch(`http://localhost:8001/v1/movies/occupation/${user.userId}`);
                const data = await response.json();
                setOccupationMovies(data.movies);
                setUserOccupation(data.occupation);
            } catch (error) {
                console.error('Error fetching occupation movies:', error);
            }
        }

        if (isloggedIn && user) {
            fetchOccupationMovies();
        }
    }, [user, isloggedIn]);

    return (
        <div className="max-w-screen-lg mx-auto w-full grid grid-cols-1 gap-10 pt-32 px-4 lg:px-0">
            <div className='grid grid-cols-1 gap-4'>
                <h1 className="text-4xl font-bold"><span className="text-pink-500">FlickFolio: Your Personalized Movie Collection</span></h1>
                <p className="text-lg">
                    We offer a personalized movie collection just for you.<br />
                    Enjoy the best picks, trendy movies, and hidden gems all in one place, tailored to your tastes.
                </p>
                <p className="text-lg">
                    FlickFolio combines 'Flick', meaning 'movie', and 'Folio', meaning 'portfolio'.<br />
                    It signifies a collection of various movies, providing a personalized movie recommendation service tailored to your preferences.
                </p>
            </div>

            <div className='grid grid-cols-1 gap-4'>
                <h2 className="text-2xl font-bold">How about this movie? It's one you haven't watched yet.</h2>
                {isloggedIn ? (
                    <MovieGrid movies={knnMovies} />
                ) : (
                    <p className="text-lg"><span className="text-pink-500">Please log in to get personalized recommendations.</span></p>
                )}
            </div>

            <div className='grid grid-cols-1 gap-4'>
                <h2 className="text-2xl font-bold">Top 10 Popular Movies (Last Month)</h2>
                <MovieSlider movies={popularMovies} />
            </div>

            <div className='grid grid-cols-1 gap-4'>
                <h2 className="text-2xl font-bold">
                    At <span className="text-pink-500">{userAge}</span> years old, these movies are a hit!<br />
                    Check out the top 10 movies loved by people your age.
                </h2>
                {isloggedIn ? (
                    <MovieGrid movies={ageMovies} />
                ) : (
                    <p className="text-lg"><span className="text-pink-500">Please log in to see movies loved by people your age.</span></p>
                )}
            </div>

            <div className='grid grid-cols-1 gap-4'>
                <h2 className="text-2xl font-bold">
                    People with your occupation, <span className="text-pink-500">{userOccupation}</span>, love these movies!<br />
                    Check out the top 10 movies enjoyed by professionals in your field.
                </h2>
                {isloggedIn ? (
                    <MovieGrid movies={occupationMovies} />
                ) : (
                    <p className="text-lg"><span className="text-pink-500">Please log in to see movies enjoyed by professionals in your field.</span></p>
                )}
            </div>
        </div>
    );
};

export default Home;
