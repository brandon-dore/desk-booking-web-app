import React from "react";
import { Typography, Container } from '@mui/material';

export const NotFound = () => {
  return (
    <>
      <Container
        sx={{
          width: "300px",
          margin: "0 auto",
          marginTop: "15%",
        }}
      >
        <Typography variant='h1' sx={{ fontSize: "80px", fontWeight: 800, textAlign: "center" }}>
          404
        </Typography>
        <Typography variant='h2' sx={{ fontSize: "25px", textAlign: "center" }}>
          Page Not Found
        </Typography>
        <Typography
          sx={{
            textAlign: "center",
            fontSize: "12px",
          }}
        >
          The Page you are looking for doesn't exist or an other error occured.
          Go to <a href="/">Home Page.</a>
        </Typography>
      </Container>
    </>
  );
};
