import AdminDashboard from "./AdminDashboard";
import UserDashboard from "./UserDashboard";
import HRDashboard from "./HRDashboard";
import Navbar from './../components/Navbar';

export default function Dashboard({ onLogout }) {
  const role = localStorage.getItem("role");

  return (
    <>
      <Navbar onLogout={onLogout} />
      {role === "admin" ? <AdminDashboard /> : role === "hr" ? <HRDashboard /> : <UserDashboard />}
    </>
  );
}
