import SOCDashboard from "./SOCDashboard";
import CompanyPortal from "./CompanyPortal";
import HRDashboard from "./HRDashboard";

export default function Dashboard({ onLogout }) {
  const role = localStorage.getItem("role");

  return (
    <>
      {role === "admin" ? (
        <SOCDashboard />
      ) : (
        <CompanyPortal />
      )}
    </>
  );
}
