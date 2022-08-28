import React, { useEffect, useState } from "react";
import TopBar from "../auth/TopBar";
import APIService from "../services/api.service";
import { experimentalStyled as styled } from "@mui/material/styles";
import { Box, Paper, Grid, Button, Stack, Modal, Typography  } from "@mui/material";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const DeskBooking = () => {
  const [user, setUser] = useState(undefined);
  const [rooms, setRooms] = useState(undefined);
  const [desks, setDesks] = useState(undefined);
  const [open, setOpen] = React.useState(false);
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

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const getDesks = (e) => {
    const roomId = e.currentTarget.getAttribute("room-id");
    setCurrentRoom(roomId);
    APIService.getDesks(roomId).then(
      (response) => {
        console.log(response);
        setDesks(response.data);
      },
      (error) => {
        console.log(error);
      }
    );
  };

  const openBooking = () => {
    console.log("hERe");
  };

  return (
    <>
      <TopBar />
      <Box sx={{ mx: 5 }}>
        {rooms ?
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
            </Box> : <p>no rooms</p>
            
        }
        {desks &&
            <Box sx={{ m: 2, pt: 3, flexGrow: 1 }}>
              <Grid
                container
                spacing={{ xs: 2, md: 3 }}
                columns={{ xs: 4, sm: 8, md: 12 }}
              >
                {Array.from(desks).map((desk) => (
                  <Grid xs={2} sm={4} md={4} key={desk.id}>
                    <Item
                      sx={{ "&:hover": { cursor: "pointer" } }}
                      onClick={handleOpen}
                    >
                      {desk.number}
                    </Item>
                  </Grid>
                ))}
              </Grid>
            </Box>
                }
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              Text in a modal
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
              Duis mollis, est non commodo luctus, nisi erat porttitor ligula.
            </Typography>
          </Box>
        </Modal>
      </Box>
    </>
  );
};

export default DeskBooking;
