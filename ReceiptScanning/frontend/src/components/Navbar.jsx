import { Link } from 'react-router-dom';

function Navbar({ user, onLogout }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/dashboard">💰 Finance Tracker</Link>
      </div>
      <div className="navbar-menu">
        <span className="navbar-user">Salut, {user?.username}</span>
        <button onClick={onLogout} className="btn-logout">
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;