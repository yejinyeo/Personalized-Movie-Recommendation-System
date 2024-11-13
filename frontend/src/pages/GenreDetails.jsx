// 예진이가 작성한 부분
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import MovieList from '../components/MovieList';

const GenreDetails = () => {
    const { genre } = useParams();
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        const fetchMoviesByGenre = async () => {
            try {
                const response = await fetch(`http://localhost:8001/v1/movies/genre/${genre}`);
                const data = await response.json();
                setMovies(data);
            } catch (error) {
                console.error('Error fetching movies by genre:', error);
            }
        };

        fetchMoviesByGenre();
    }, [genre]);

    return (
        <div className="">
            <div className='max-w-screen-lg w-full mx-auto grid grid-cols-1 gap-10 px-4 lg:px-0 pt-32'>
                <div className='flex flex-col md:flex-row gap-4 w-full'>
                    <div className='flex flex-col *:py-3 text-slate-400 font-bold divide-y-[1px] divide-slate-600 divide-opacity-50 grow'>
                        <h1 className="text-4xl first:pt-0 text-slate-100 font-bold">Discover the Best Rated <span className="text-pink-500">{genre}</span> Movies!<br /> 
                        Here are all the movies in this genre.</h1>
                    </div>
                </div>

                <div className='grid grid-cols-1 gap-4'>
                    <MovieList movies={movies} />
                </div>
            </div>
        </div>
    );
};

export default GenreDetails;
