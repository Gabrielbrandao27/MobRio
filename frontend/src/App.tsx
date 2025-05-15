import { Route, Routes } from 'react-router-dom';
import NavbarLayout from './components/NavbarLayout';
import HomePage from './pages/HomePage';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import RouteStopRegisterPage from './pages/RouteStopRegisterPage';

function App() {
  return (
    <Routes>
      {/* Rotas sem Navbar */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />

      {/* Rotas com Navbar */}
      <Route element={<NavbarLayout />}>
        <Route path="/home" element={<HomePage />} />
        <Route path="/route-stop-register" element={<RouteStopRegisterPage />} />
      </Route>
    </Routes>
  );
}

export default App;
