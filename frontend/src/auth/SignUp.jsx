import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button, TextField, Grid, Container, Box, CssBaseline, Typography } from "@mui/material";
import TopBar from "./TopBar";
import AuthService from "../services/auth.service";

const defaultValues = {
  username: "",
  email: "",
  password: "",
};

export const SignUp = () => {
  const navigate = useNavigate();

  const [formValues, setFormValues] = useState(defaultValues);

  const [error, setError] = useState({
    loading: false,
    message: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormValues({
      ...formValues,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError({
      message: "",
      loading: true,
    });
    AuthService.register(formValues).then(
      () => {
        navigate("/");
      },
      () => {
        const resMessage =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString();
        setError({
          loading: false,
          message: resMessage,
        });
      }
    );
  };

  return (
    <>
    <TopBar />
    <Container component="main" maxWidth="xs">
      <CssBaseline />
     
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
         <Typography component="h1" variant="h5">
            Sign up
          </Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            onChange={handleInputChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="email"
            label="Email"
            type="email"
            id="email"
            autoComplete="email"
            onChange={handleInputChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            onChange={handleInputChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={error.loading}
            sx={{ mt: 3, mb: 2 }}
          >
            Sign Up
          </Button>
          <Grid container>
            <Grid item>
              <Link to="/" >
                {"Already have an account? Login here."}
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
    </> 
  );
};
