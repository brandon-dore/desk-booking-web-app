import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Button,
  TextField,
  Grid,
  Container,
  Box,
  CssBaseline,
  Typography,
} from "@mui/material";
import TopBar from "./TopBar";
import AuthService from "../services/auth.service";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from "yup";

export const Login = () => {
  const [loading, setLoading] = useState(false);

  let navigate = useNavigate();

  const validationSchema = Yup.object().shape({
    username: Yup.string()
      .required("Username is required"),
    password: Yup.string()
      .required("Password is required")
  });

  

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(validationSchema),
  });

  const onSubmit = data => {
    setLoading(true)
    AuthService.login(data).then(
      () => {
        navigate("/home");
      },
      () => {
        setLoading(false)
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
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              sx={{ mt: 3, mb: 2 }}
              onClick={handleSubmit(onSubmit)}
            >
              Sign In
            </Button>
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
