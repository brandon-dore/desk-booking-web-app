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
  Card,
  CardContent,
  CardActions,
  Modal,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/auth.service";
import APIService from "../services/api.service";
import DeskIcon from "@mui/icons-material/Desk";
import Avatar from "@mui/material/Avatar";
import sloth from "../../avatar.png";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 200,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export default function CommonAppBar(props) {
  const navigate = useNavigate();

  const [modalOpen, setModalOpen] = useState(false);

  const [currentUser, setCurrentUser] = useState({
    isLoggedIn: false,
    admin: false,
  });

  const [anchorElUser, setAnchorElUser] = React.useState(null);

  useEffect(() => {
    APIService.getUserInfo().then(
      (response) => {
        console.log(response);
        setCurrentUser({
          isLoggedIn: true,
          admin: response.data.admin,
          username: response.data.username,
          email: response.data.email,
        });
      },
      (error) => {
        console.log(error);
      }
    );
  }, []);

  const handleModalOpen = (desk) => {
    if (!desk.booked) {
      setModalOpen(true);
    }
  };
  const handleModalClose = () => setModalOpen(false);

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
    navigate(0);
  };

  const card = (
    <React.Fragment>
      <Box sx={style}>
        <CardContent>
          <Avatar alt="Sloth Avatar" src={sloth} />

          <Typography variant="h3" component="div">
            {currentUser.username}
          </Typography>
          <Typography sx={{ mb: 1.5 }} color="text.secondary">
            {currentUser.admin ? "Admin" : "User"}
          </Typography>
          <Typography variant="body2">Email: {currentUser.email}</Typography>
        </CardContent>
      </Box>
    </React.Fragment>
  );

  const container = (
    <Container maxWidth="false">
      <Toolbar disableGutters>
        <DeskIcon sx={{ display: { xs: "none", md: "flex" }, mr: 1 }} />
        <Typography
          variant="h5"
          noWrap
          component="a"
          onClick={() => navigate("/")}
          sx={{
            "&:hover": {
              cursor: "pointer",
            },
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
          {currentUser.admin && (
            <Button
              onClick={() => navigate("/admin")}
              sx={{ my: 2, color: "white", display: "block" }}
            >
              Admin Panel
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
                <Avatar alt="Sloth Avatar" src={sloth} />
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
              <MenuItem onClick={handleModalOpen}>My Account</MenuItem>
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
          </Box>
        )}
      </Toolbar>
      <Modal
        open={modalOpen}
        onClose={handleModalClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Card variant="outlined">{card}</Card>
      </Modal>
    </Container>
  );

  return (
    <>
        <AppBar
        position={props.commonAppBar && "staic"}
          sx={{
            "& .RaAppBar-title": {
              flex: 1,
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
              overflow: "hidden",
            },
            height: "65px",
          }}
          {...props}
        >
          {container}
        </AppBar>
    </>
  );
}
