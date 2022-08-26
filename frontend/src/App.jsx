import {
  Route,
  Routes,
  Navigate,
  useLocation
} from "react-router-dom";
import Home from "./desk-booking/Home";
import { DeskBookingAdmin } from "./admin/DeskBookingAdmin";
import { Login } from "./auth/Login";
import { SignUp } from "./auth/SignUp";
import { useEffect, useState, useLayoutEffect } from "react";
import AuthService from "./services/auth.service";

const App = () => {
  let location = useLocation();

  const [currentUser, setCurrentUser] = useState(undefined);

  useEffect(() => {
    const user = AuthService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
      console.log(user)
    }
  }, []);

  useLayoutEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));
    if (user) {
      const decodedJwt = JSON.parse(atob(user.access_token.split(".")[1]));
      if (decodedJwt.exp * 1000 < Date.now()) {
        AuthService.logout();
        setCurrentUser(undefined);
      }
    }
  }, [location]);

  return (
      <Routes>
        <Route exact path="/" element={<Login />} />
        <Route
          path="/admin/*"
          element={
            <RequireAuth redirectTo="/">
              <DeskBookingAdmin />
            </RequireAuth>
          }
        />
        <Route
          path="/home"
          element={
            <RequireAuth redirectTo="/">
              <Home />
            </RequireAuth>
          }
        />
        <Route exact path="/sign-up" element={<SignUp />} />
      </Routes>
  );
};

function RequireAuth({ children, redirectTo }) {
  return (localStorage.getItem("user").access_token == null) ? children : <Navigate to={redirectTo} />;
}

export default App;
