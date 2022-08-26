import {
  IconButton,
  Button,
  Typography,
  Toolbar,
  AppBar,
  Menu,
  MenuItem,
} from "@mui/material";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/auth.service";
import DeskIcon from '@mui/icons-material/Desk';

export default function TopBar() {
  const navigate = useNavigate();
  
  const [currentUser, setCurrentUser] = useState({
    username: "",
    isLoggedIn: false,
  });
  const [anchorEl, setAnchorEl] = React.useState(null);

  useEffect(() => {
    const user = AuthService.getCurrentUser();
    if (user !== "undefined" && user !== null) {
      // Check if JWT is valid?
      setCurrentUser({ username: currentUser, isLoggedIn: true });
    }
  }, []);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    setAnchorEl(null);
    AuthService.logout();
    navigate("/")
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <DeskIcon/>
        </IconButton>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Desk Booking App
        </Typography>
        {!currentUser.isLoggedIn && <Button color="inherit" href="/">Login</Button>}
        {currentUser.isLoggedIn && (
          <div>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              color="inherit"
            >
              <AccountCircleIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleClose}>My Account</MenuItem>
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
          </div>
        )}
      </Toolbar>
    </AppBar>
  );
}
