import React, { useEffect, useState } from "react";
import TopBar from "../auth/TopBar";
import APIService from "../services/api.service";
import { experimentalStyled as styled } from "@mui/material/styles";
import { Box, Paper, Grid, Button, Stack } from "@mui/material";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));

const DeskBooking = () => {
  const [user, setUser] = useState(undefined);
  const [rooms, setRooms] = useState(undefined);
  const [currentRoom, setCurrentRoom] = useState(undefined);

  useEffect(() => {
    APIService.getUserInfo().then(
      (response) => {
        setUser(response.data);
      },
      (error) => {
        console.log(error);
      }
    );
    APIService.getRooms().then(
      (response) => {
        console.log(response.data);
        setRooms(response.data);
      },
      (error) => {
        console.log(error);
      }
    );
  }, []);

  const getDesks = (e) => {
    e.currentTarget.getAttribute("room-id")
    
  }

  return (
    <>
      <TopBar />
      <Box sx={{ mx: 5 }}>
        {rooms ? (
          <>
            <Box sx={{ m: 1, pt: 1, flexGrow: 1 }}>
              <Stack direction="row" spacing={5}>
                {Array.from(rooms).map((room) => (
                  <Button
                    room-id={room.id}
                    variant={room.id == currentRoom ? "contained" : "outlined"}
                    size="large"
                    style={{ minWidth: "200px" }}
                    onClick={getDesks}
                  >
                    Room {room.name}
                  </Button>
                ))}
              </Stack>
            </Box>
            <Box sx={{ m: 2, pt: 3, flexGrow: 1 }}>
              <Grid
                container
                spacing={{ xs: 2, md: 3 }}
                columns={{ xs: 4, sm: 8, md: 12 }}
              >
                {Array.from(Array(6)).map((_, index) => (
                  <Grid xs={2} sm={4} md={4} key={index}>
                    <Item>xs=2</Item>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </>
        ) : (
          <p>no</p>
        )}
      </Box>
    </>
  );
};

export default DeskBooking;
