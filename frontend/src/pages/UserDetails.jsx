import React, { useEffect, useState } from 'react';

import MovieList from '../components/MovieList';
import MovieSlider from '../components/MovieSlider';

const UserDetails = ({ user }) => {
    const [movies, setMovies] = useState([]);
    const [favoriteGenreMovies, setFavoriteGenreMovies] = useState([]);
    const [favoriteGenre, setFavoriteGenre] = useState('');

    useEffect(() => {
        async function fetchMovies() {
            try {
                const response = await fetch(`http://localhost:8001/v1/user/${user.userId}/rated`);
                const data = await response.json();
                setMovies(data);
            } catch (error) {
                console.error('Error fetching movies:', error);
            }
        }

        fetchMovies();
    }, [user]);

    useEffect(() => {
        async function fetchFavoriteGenreMovies() {
            try {
                const response = await fetch(`http://localhost:8001/v1/movies/favorite-genre/${user.userId}`);
                const data = await response.json();
                setFavoriteGenreMovies(data.movies);
                setFavoriteGenre(data.favorite_genre);
            } catch (error) {
                console.error('Error fetching favorite genre movies:', error);
            }
        }

        fetchFavoriteGenreMovies();
    }, [user]);

    return (
        <div className="max-w-screen-lg mx-auto w-full grid grid-cols-1 gap-10 pt-32 px-4 lg:px-0">
            {user === null ? <h1 className="text-2xl font-bold">User not found</h1> :
                <>
                    <div className='grid grid-cols-1 gap-4'>
                        <h1 className="text-4xl font-bold">Welcome User {user.userId}!</h1>
                        <p className="text-xl font-normal">You have rated <span className="text-pink-500">{movies.length}</span> movies</p>
                        <ul className="list-disc pl-4">
                            <li>User ID: {user.userId}</li>
                            <li>Occupation: {user.occupation}</li>
                            <li>Age: {user.age}</li>
                            <li>Gender: {user.gender}</li>
                            <li>Zip Code: {user.ZIPCODE}</li>
                        </ul>
                    </div>

                    <div className='grid grid-cols-1 gap-4'>
                        <h2 className="text-2xl font-bold">
                            You watch a lot of <span className="text-pink-500">{favoriteGenre}</span> movies!<br />
                            Check out the top 10 best movies in this genre.
                        </h2>
                        <MovieSlider movies={favoriteGenreMovies} />
                    </div>

                    <div className='grid grid-cols-1 gap-4'>
                        <h2 className="text-2xl font-bold">Recently Rated Movies</h2>
                        <MovieList movies={movies} />
                    </div>
                </>
            }
        </div>
    );
};

export default UserDetails;
