import React, { useEffect, useState } from "react";
import TopBar from "./components/header/CommonAppBar";
import AuthService from "./components/services/auth.service";
import { Box } from "@mui/material";
import { Link } from "react-router-dom";

const Home = () => {
    const [currentUser, setCurrentUser] = useState(undefined);


  useEffect(() => {
    const user = AuthService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
    }
  }, []);

  return (
    <>
      <TopBar />
      <Box sx={{ mx:5 }}>
        {currentUser ? <p>Welcome Back. Click <Link to="/desk-booking">here</Link> to book a desk</p>:<p><Link to="/login">Login</Link> to view content</p>}
    </Box>
    </>
  );
};

export default Home;
