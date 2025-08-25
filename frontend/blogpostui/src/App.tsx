import { JSX } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, BrowserRouter } from "react-router-dom";
import Login from "./routes/Login";
import Home from "./routes/Home";
import Signup from "./routes/Signup";
import Dashboard from "./routes/Dashboard";
import BlogDetail from "./routes/BlogDetail"
import './index.css'; // Import your main CSS file

// Helper to protect routes
const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const token = localStorage.getItem("token");
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home/>} />
      <Route path="/login" element={<Login/>} />
      <Route path="/signup" element={<Signup/>} />
<Route path="/dashboard" element={<Dashboard/>} />
        <Route path="/blog/:id" element={<BlogDetail />} />
    </Routes>
    </BrowserRouter>

  );
}
export default App;