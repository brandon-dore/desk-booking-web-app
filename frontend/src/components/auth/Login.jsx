import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  TextField,
  Grid,
  Container,
  Box,
  CssBaseline,
  Typography,
} from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import TopBar from "../header/CommonAppBar";
import AuthService from "../services/auth.service";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from "yup";

export const Login = () => {
  let navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(undefined);

  const validationSchema = Yup.object().shape({
    username: Yup.string().required("Username is required"),
    password: Yup.string().required("Password is required"),
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(validationSchema),
  });

  const onSubmit = (data) => {
    setLoading(true);
    AuthService.login(data).then(
      () => {
        navigate("/");
      },
      () => {
        setLoading(false);
        setResponse("Login failed. Please try again.");
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
            Sign in
          </Typography>
          <Box sx={{ mt: 1 }}>
            <form onSubmit={handleSubmit(onSubmit)}>
              <TextField
                required
                id="username"
                name="username"
                label="Username"
                fullWidth
                margin="dense"
                {...register("username")}
                error={errors.username ? true : false}
              />
              <Typography variant="inherit" color="textSecondary">
                {errors.username?.message}
              </Typography>
              <TextField
                required
                id="password"
                name="password"
                label="Password"
                type="password"
                fullWidth
                margin="dense"
                {...register("password")}
                error={errors.password ? true : false}
              />
              <Typography variant="inherit" color="textSecondary">
                {errors.password?.message}
              </Typography>
              <Typography variant="inherit" color="textSecondary">
                {response}
              </Typography>
              <LoadingButton
                type="submit"
                fullWidth
                variant="contained"
                loading={loading}
                sx={{ mt: 3, mb: 2 }}
                onClick={handleSubmit(onSubmit)}
              >
                Sign In
              </LoadingButton>
            </form>
            <Grid container>
              <Grid item>
                <Link to="/sign-up">
                  {"Don't have an account? Register here."}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </>
  );
};
