import React, { useState } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';

import './App.css';

import Home from './pages/Home';
import MovieDetails from './pages/MovieDetails';
import MovieSearch from './pages/MovieSearch';
import UserDetails from './pages/UserDetails';
import GenreDetails from './pages/GenreDetails'; // 추가된 부분

import Footer from './components/Footer';
import Nav from './components/Nav';

function App() {
    const location = useLocation();
    const [isloggedIn, setIsLoggedIn] = useState(localStorage.getItem('isloggedIn') === 'true');
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));

    return (
        <div className="App text-slate-50 bg-slate-950 min-w-96">
            <Nav user={user} setUser={setUser} isloggedIn={isloggedIn} setIsLoggedIn={setIsLoggedIn} />

            <div className='mx-auto'>
                <Routes location={location}>
                    <Route key={location.pathname} path='/' element={<Home user={user} isloggedIn={isloggedIn} />} />
                    <Route key={location.pathname} path='/search' element={<MovieSearch />} />
                    <Route key={location.pathname} path='/movie/:id' element={<MovieDetails movieId={location.pathname.split('/')[2]} user={user} />} />
                    <Route key={location.pathname} path='/user/:id' element={<UserDetails user={user} />} />
                    <Route key={location.pathname} path='/genre/:genre' element={<GenreDetails />} /> {/* 추가된 부분 */}
                </Routes>
            </div>

            <Footer />
        </div>
    );
}

export default App;
