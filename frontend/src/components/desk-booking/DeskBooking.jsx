import React, { useEffect, useState } from "react";
import TopBar from "../header/CommonAppBar";
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
  const [openedDesk, setOpenedDesk] = useState(undefined);

  const [currentRoom, setCurrentRoom] = useState(undefined);
  const [currentDate, setCurrentDate] = useState(moment());

  let currentDesk = 0;

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

  const handleOpen = (desk) => {
    if (!desk.booked) {
      setOpen(true);
      setOpenedDesk(desk.id);
    }
  };
  const handleClose = () => setOpen(false);

  const getDesks = () => {
    APIService.getDesks(currentRoom).then(
      (response) => {
        currentDesk = 0;
        setDesks(response.data);
        setCurrentDate(moment());
        getBookings();
      },
      (error) => {
        console.log(error);
      }
    );
  };

  const updateDesks = (id, update_key, update_value) => {
    setDesks((prevDesks) => {
      return prevDesks.map((desk) => {
        return desk.id === id ? { ...desk, [update_key]: update_value } : desk;
      });
    });
  };

  const getBookings = () => {
    APIService.getBookings(currentDate.format("YYYY-MM-DD"), currentRoom).then(
      (response) => {
        const bookingsResponse = response.data;
        setBookings(bookingsResponse);
        desks.forEach((desk) => {
          updateDesks(desk.id, "booked", false);
          updateDesks(desk.id, "booked_user", undefined);
        });
        if (bookingsResponse.length > 0) {
          desks.forEach((desk) => {
            bookingsResponse.forEach((booking) => {
              if (desk.id == booking.desk_id) {
                updateDesks(desk.id, "booked", true);
                APIService.getUser(booking.user_id).then(
                  (user_response) => {
                    updateDesks(
                      desk.id,
                      "booked_user",
                      user_response.data.username
                    );
                  },
                  (error) => {
                    console.log(error);
                  }
                );
              }
            });
          });
        }
      },
      (error) => {
        console.log(error);
      }
    );
  };

  const bookDesk = () => {
    APIService.makeBooking({
      date: currentDate.format("YYYY-MM-DD"),
      user_id: user.id,
      desk_id: openedDesk,
      approved_status: false,
    }).then(
      () => {
        handleClose();
        getBookings();
      },
      () => {
        console.log("error");
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
                  Room: {room.name}
                </Button>
              ))}
            </Stack>
          </Box>
        ) : (
          <p>no rooms</p>
        )}
        {desks && (
          <Box sx={{ m: 4, pt: 3, flexGrow: 1 }}>
            <Box sx={{ mb: 5 }}>
              <LocalizationProvider
                dateAdapter={AdapterMoment}
                sx={{ mb: 100 }}
              >
                <DesktopDatePicker
                  label="Date"
                  inputFormat="MM/DD/YYYY"
                  disablePast
                  value={currentDate}
                  onChange={(newDate) => {
                    setCurrentDate(newDate);
                  }}
                  renderInput={(params) => <TextField {...params} />}
                  sx={{ mb: 1000 }}
                />
              </LocalizationProvider>
            </Box>
            <Box
              sx={{
                display: "grid",
                gridAutoFlow: "column",
                gridTemplateColumns: "repeat(8, 11.6vw)",
                gridTemplateRows: "repeat(4, 11.6vw)",
                gridTemplateAreas: "none",
              }}
            >
              {[...Array(32)].map((_, index) => {
                let isDesk = false;

                let desk;
                if (index + ((1 / 4) % 3) !== 0 && desks.length > currentDesk) {
                  isDesk = true;
                  desk = desks[currentDesk];
                  currentDesk++;
                }

                return (
                  <>
                    {isDesk ? (
                      <Paper
                        sx={{
                          transition: "all 0.15s ease-out",
                          "&:hover": desk.booked
                            ? {}
                            : {
                                cursor: "pointer",
                                transform: "scale(1.06)",
                                transition: "all 0.15s ease-in",
                              },
                          border: 2,
                          borderBottomStyle: "solid",
                          borderColor: desk.booked ? "red" : "black",
                          textAlign: "center",
                          display: "flex",
                          justifyContent: "center",
                          alignItems: "center",
                          fontSize: "1em",
                          gridGap: "1px",
                        }}
                        onClick={() => handleOpen(desk)}
                      >
                        {desk.number}
                        {desk.booked && (
                          <p>Desk booked by {desk.booked_user}</p>
                        )}
                      </Paper>
                    ) : (
                      <Box> </Box>
                    )}
                  </>
                );
              })}
            </Box>
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
              By clicking the button below, you are confirming that you will sit
              at this desk on {currentDate && currentDate.format("YYYY-MM-DD")}
            </Typography>
            <br />
            <Button variant="contained" onClick={bookDesk}>
              Book Desk
            </Button>
          </Box>
        </Modal>
      </Box>
    </>
  );
};

export default DeskBooking;
