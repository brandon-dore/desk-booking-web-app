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
import UserService from "../services/user.service";
import DeskIcon from '@mui/icons-material/Desk';

export default function TopBar() {
  const navigate = useNavigate();
  
  const [currentUser, setCurrentUser] = useState({
    isLoggedIn: false,
    admin: false
  });

  const [anchorEl, setAnchorEl] = React.useState(null);

  useEffect(() => {
    UserService.getUserInfo().then(
      (response) => {
        setCurrentUser({ isLoggedIn: true, admin: response.data.admin });
      },
      (error) => {
        console.log(error);
      }
    );
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
              {currentUser.admin && <MenuItem onClick={() => navigate("/admin")}>Admin Panel</MenuItem>}
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
          </div>
        )}
      </Toolbar>
    </AppBar>
  );
}
