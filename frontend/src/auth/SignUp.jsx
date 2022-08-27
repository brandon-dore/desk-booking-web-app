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


export const SignUp = () => {
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const validationSchema = Yup.object().shape({
    username: Yup.string()
      .required("Username is required")
      .min(6, "Username must be at least 6 characters")
      .max(20, "Username must not exceed 20 characters"),
    email: Yup.string().required("Email is required").email("Email is invalid"),
    password: Yup.string()
      .required("Password is required")
      .min(6, "Password must be at least 6 characters")
      .max(40, "Password must not exceed 40 characters"),
    confirmPassword: Yup.string()
      .required("Confirm Password is required")
      .oneOf([Yup.ref("password"), null], "Confirm Password does not match"),
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(validationSchema),
  });


  const onSubmit = data => {
    setLoading(true);
    delete data.confirmPassword
    AuthService.signUp(data).then(
      () => {
        navigate("/");
      },
      () => {
        setLoading(false);
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
          <Box
            sx={{ mt: 1 }}
          >
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
              id="email"
              name="email"
              label="Email"
              fullWidth
              margin="dense"
              {...register("email")}
              error={errors.email ? true : false}
            />
            <Typography variant="inherit" color="textSecondary">
              {errors.email?.message}
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
            <TextField
              required
              id="confirmPassword"
              name="confirmPassword"
              label="Confirm Password"
              type="password"
              fullWidth
              margin="dense"
              {...register("confirmPassword")}
              error={errors.confirmPassword ? true : false}
            />
            <Typography variant="inherit" color="textSecondary">
              {errors.confirmPassword?.message}
            </Typography>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              sx={{ mt: 3, mb: 2 }}
              onClick={handleSubmit(onSubmit)}
            >
              Sign Up
            </Button>
            <Grid container>
              <Grid item>
                <Link to="/">{"Already have an account? Login here."}</Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </>
  );
};
