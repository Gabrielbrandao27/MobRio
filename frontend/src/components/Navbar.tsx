import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{ padding: '10px', borderBottom: '1px solid #ddd' }}>
      <Link to="/home" style={{ marginRight: '20px' }}>
        Home
      </Link>
      <Link to="/route-stop-register" style={{ marginRight: '20px' }}>
        Cadastro de Ônibus
      </Link>
    </nav>
  );
}

export default Navbar;
