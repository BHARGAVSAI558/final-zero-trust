import AdminDashboard from "./AdminDashboard";
import UserDashboard from "./UserDashboard";
import Navbar from './../components/Navbar';

export default function Dashboard({ onLogout }) {
  const role = localStorage.getItem("role");

  return (
    <>
      <Navbar onLogout={onLogout} />
      {role === "admin" ? <AdminDashboard /> : <UserDashboard />}
    </>
  );
}
