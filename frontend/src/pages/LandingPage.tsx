import { Link } from 'react-router-dom';

function LandingPage() {
  return (
    <div className="landing-container">
      <h1>Bem-vindo ao MobRio!</h1>
      <p>Monitore ônibus em tempo real na cidade do Rio de Janeiro.</p>
      <div>
        <Link to="/login">
          <button>Login</button>
        </Link>
        <Link to="/register">
          <button>Registrar</button>
        </Link>
      </div>
    </div>
  );
}

export default LandingPage;
