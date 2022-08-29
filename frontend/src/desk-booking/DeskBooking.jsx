import React, { useEffect, useState } from "react";
import TopBar from "../auth/TopBar";
import APIService from "../services/api.service";
import { experimentalStyled as styled } from "@mui/material/styles";
import {
  Box,
  Paper,
  Grid,
  Button,
  Stack,
  Modal,
  Typography,
  TextField,
} from "@mui/material";
import { LocalizationProvider, DesktopDatePicker } from "@mui/x-date-pickers";
import { AdapterMoment } from "@mui/x-date-pickers/AdapterMoment";
import moment from "moment";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

const DeskBooking = () => {
  const [user, setUser] = useState(undefined);
  const [rooms, setRooms] = useState(undefined);
  const [desks, setDesks] = useState(undefined);
  const [bookings, setBookings] = useState(undefined);
  const [open, setOpen] = useState(false);
  const [currentRoom, setCurrentRoom] = useState(undefined);
  const [currentDate, setCurrentDate] = useState(undefined);

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
        setRooms(response.data);
      },
      (error) => {
        console.log(error);
      }
    );
  }, []);

  useEffect(() => {
    if (typeof currentRoom !== "undefined") {
      getDesks();
    }
  }, [currentRoom]);

  useEffect(() => {
    if (typeof currentDate !== "undefined") {
      getBookings();
    }
  }, [currentDate]);

  const handleOpen = (booked) => {
    if (!booked) {
      setOpen(true);
    }
  };
  const handleClose = () => setOpen(false);

  const getDesks = (e) => {
    APIService.getDesks(currentRoom).then(
      (response) => {
        setDesks(response.data);
        setCurrentDate(moment());
        getBookings();
      },
      (error) => {
        console.log(error);
      }
    );
  };

  const updateDesks = (id, bookingStatus) => {
    setDesks((prevDesks) => {
      return prevDesks.map((desk) => {
        return desk.id === id ? { ...desk, booked: bookingStatus } : desk;
      });
    });
  };

  const getBookings = () => {
    APIService.getBookings(currentDate.format("YYYY-MM-DD"), currentRoom).then(
      (response) => {
        const bookingsResponse = response.data;
        setBookings(bookingsResponse);
        desks.forEach((desk) => {
          updateDesks(desk.id, false);
        });
        if (bookingsResponse.length > 0) {
          desks.forEach((desk) => {
            bookingsResponse.forEach((booking) => {
              if (desk.id == booking.desk_id) {
                updateDesks(desk.id, true);
              }
            });
          });
        }
        console.log(desks);
      },
      (error) => {
        console.log(error);
      }
    );
  };

  return (
    <>
      <TopBar />
      <Box sx={{ mx: 5 }}>
        {rooms ? (
          <Box sx={{ m: 1, pt: 1, flexGrow: 1 }}>
            <Stack direction="row" spacing={5}>
              {Array.from(rooms).map((room) => (
                <Button
                  room-id={room.id}
                  variant={room.id == currentRoom ? "contained" : "outlined"}
                  size="large"
                  style={{ minWidth: "200px" }}
                  onClick={(e) => {
                    setCurrentRoom(e.currentTarget.getAttribute("room-id"));
                  }}
                >
                  Room {room.name}
                </Button>
              ))}
            </Stack>
          </Box>
        ) : (
          <p>no rooms</p>
        )}
        {desks && (
          <Box sx={{ m: 4, pt: 3, flexGrow: 1 }}>
            <Grid
              container
              spacing={{ xs: 2, md: 3 }}
              columns={{ xs: 4, sm: 8, md: 12}}
            >
              <Grid xs={12} sm={12} md={12} mb={2}>
                <LocalizationProvider dateAdapter={AdapterMoment}>
                  <DesktopDatePicker
                    label="Date"
                    inputFormat="MM/DD/YYYY"
                    value={currentDate}
                    onChange={(newDate) => {
                      setCurrentDate(newDate);
                    }}
                    renderInput={(params) => <TextField {...params} />}
                  />
                </LocalizationProvider>
              </Grid>
              {Array.from(desks).map((desk) => (
                <Grid xs={2} sm={4} md={4} key={desk.id} id={desk.id}>
                  <Item
                    sx={{
                      "&:hover": desk.booked ? {} : { cursor: "pointer" },
                      border: 1,
                      borderColor: desk.booked ? "red" : "#fff",
                    }}
                    onClick={() => handleOpen(desk.booked)}
                  >
                    {desk.number}
                  </Item>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              Book Desk
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
              By clicking the button below, you are confirming that you will sit at this desk on the xx/xx/xxxx
            </Typography>
            <br/>
            <Button variant="contained">Book Desk</Button>
          </Box>
        </Modal>
      </Box>
    </>
  );
};

export default DeskBooking;
