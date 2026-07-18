import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';

export default function DashboardLayout() {
  return (
    <>
      <Navbar />
      <main className="container animate-fade-in">
        <Outlet />
      </main>
    </>
  );
}
