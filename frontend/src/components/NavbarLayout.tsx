import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

function NavbarLayout() {
  return (
    <>
      <Navbar />
      <Outlet />
    </>
  );
}

export default NavbarLayout;