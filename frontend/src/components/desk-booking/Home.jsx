import React, { useEffect, useState } from "react";
import TopBar from "../header/CommonAppBar";
import APIService from "../services/api.service";
import { Typography, Container } from "@mui/material";
import { Link } from "react-router-dom";

const Home = () => {
  const [currentUser, setCurrentUser] = useState(undefined);

  useEffect(() => {
    APIService.getUserInfo().then(
      (response) => {
        console.log(response)
        setCurrentUser({ username: response.data.username });
      },
      (error) => {
        console.log(error);
      }
    );
  }, []);

  return (
    <>
      <TopBar commonAppBar/>
      <Container
        sx={{
          width: "100%",
          margin: "0 auto",
          marginTop: "15%",
        }}
      >
        {currentUser ? (
          <>
            <Typography
              variant="h1"
              sx={{ fontSize: "80px", fontWeight: 800, textAlign: "center" }}
            >
              Hello, {currentUser.username}
            </Typography>
            <Typography
              sx={{
                textAlign: "center",
                fontSize: "17px",
              }}
            >
              Welcome Back. Click <Link to="/desk-booking">here</Link> to book a
              desk
            </Typography>
          </>
        ) : (
          <>
          <Typography
              variant="h1"
              sx={{ fontSize: "80px", fontWeight: 800, textAlign: "center" }}
            >
              Welcome
            </Typography>
          <Typography
            sx={{
              textAlign: "center",
              fontSize: "17px",
            }}
          >
            <Link to="/login">Login</Link> to view content
          </Typography>
          </>
        )}
      </Container>
    </>
  );
};

export default Home;
