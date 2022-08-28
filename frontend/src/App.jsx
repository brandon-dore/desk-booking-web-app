import { Route, Routes, Navigate, useLocation, useNavigate } from "react-router-dom";
import DeskBooking from "./desk-booking/DeskBooking";
import Home from "./Home";
import { DeskBookingAdmin } from "./admin/DeskBookingAdmin";
import { Login } from "./auth/Login";
import { SignUp } from "./auth/SignUp";
import { useEffect, useLayoutEffect } from "react";
import AuthService from "./services/auth.service";

const App = () => {
  let location = useLocation();
  let navigate = useNavigate();

  useEffect(() => {
    const user = AuthService.getCurrentUser();
    if (user) {
      console.log(user);
    }
  }, []);

  useLayoutEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));
    if (user) {
      const decodedJwt = JSON.parse(atob(user.access_token.split(".")[1]));
      if (decodedJwt.exp * 1000 < Date.now()) {
        AuthService.logout();
        navigate("/");
        navigate(0);
      }
    }
  }, [location]);

  return (
    <Routes>
      <Route exact path="/" element={<Home />} />
      <Route exact path="/login" element={<Login />} />
      <Route exact path="/sign-up" element={<SignUp />} />
      <Route
        path="/admin/*"
        element={
          <RequireAuth redirectTo="/">
            <DeskBookingAdmin />
          </RequireAuth>
        }
      />
      <Route
        path="/desk-booking"
        element={
          <RequireAuth redirectTo="/">
            <DeskBooking />
          </RequireAuth>
        }
      />
    </Routes>
  );
};

function RequireAuth({ children, redirectTo }) {
  return localStorage.getItem("user").access_token == null ? (
    children
  ) : (
    <Navigate to={redirectTo} />
  );
}

export default App;
