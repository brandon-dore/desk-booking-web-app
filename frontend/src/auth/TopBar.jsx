import {
  IconButton,
  Button,
  Typography,
  Toolbar,
  AppBar,
  Menu,
  MenuItem,
  Box,
  Container,
  Tooltip,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/auth.service";
import APIService from "../services/api.service";
import DeskIcon from "@mui/icons-material/Desk";
import Avatar from "@mui/material/Avatar";

export default function TopBar() {
  const navigate = useNavigate();

  const [currentUser, setCurrentUser] = useState({
    isLoggedIn: false,
    admin: false,
  });

  const [anchorElUser, setAnchorElUser] = React.useState(null);

  useEffect(() => {
    APIService.getUserInfo().then(
      (response) => {
        setCurrentUser({ isLoggedIn: true, admin: response.data.admin });
      },
      (error) => {
        console.log(error);
      }
    );
  }, []);


  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleLogout = () => {
    setAnchorElUser(null);
    AuthService.logout();
    navigate("/");
  };

  return (
    <AppBar position="static">
      <Container maxWidth="false">
        <Toolbar disableGutters>
          <DeskIcon sx={{ display: { xs: "none", md: "flex" }, mr: 1 }} />
          <Typography
            variant="h5"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              display: { xs: "none", md: "flex" },
              fontFamily: "monospace",
              fontWeight: 700,
              color: "inherit",
              textDecoration: "none",
            }}
          >
            Desk Booking App
          </Typography>
          <DeskIcon sx={{ display: { xs: "flex", md: "none" }, mr: 1 }} />
          <Box sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
            <Button
              onClick={() => navigate("/")}
              sx={{ my: 2, color: "white", display: "block" }}
            >
              Home
            </Button>
            {currentUser.isLoggedIn && (
              <Button
                onClick={() => navigate("/desk-booking")}
                sx={{ my: 2, color: "white", display: "block" }}
              >
                Book a Desk
              </Button>
            )}
          </Box>
          {!currentUser.isLoggedIn && (
            <Button color="inherit" onClick={() => navigate("/login")}>
              Login
            </Button>
          )}
          {currentUser.isLoggedIn && (
            <Box sx={{ flexGrow: 0 }}>
              <Tooltip title="Open settings">
                <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                  <Avatar alt="Remy Sharp" src="/static/images/avatar/2.jpg" />
                </IconButton>
              </Tooltip>
              <Menu
                sx={{ mt: "45px" }}
                id="menu-appbar"
                anchorEl={anchorElUser}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                open={Boolean(anchorElUser)}
                onClose={handleCloseUserMenu}
              >
                <MenuItem onClick={handleCloseUserMenu}>My Account</MenuItem>
                {currentUser.admin && (
                  <MenuItem onClick={() => navigate("/admin")}>
                    Admin Panel
                  </MenuItem>
                )}
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </Box>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  );
}
