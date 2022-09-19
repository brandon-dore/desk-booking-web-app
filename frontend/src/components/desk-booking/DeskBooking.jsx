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
import LoadingButton from "@mui/lab/LoadingButton";
import { useSnackbar } from "notistack";
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
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const [user, setUser] = useState(undefined);
  const [rooms, setRooms] = useState(undefined);
  const [desks, setDesks] = useState(undefined);
  const [bookings, setBookings] = useState(undefined);
  const [modalOpen, setModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const [openedDesk, setOpenedDesk] = useState({
    id: undefined,
    number: undefined,
  });

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

  const handleModalOpen = (desk) => {
    if (!desk.booked) {
      setModalOpen(true);
      setOpenedDesk({ id: desk.id, number: desk.number });
    }
  };
  const handleModalClose = () => setModalOpen(false);

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
    setLoading(true);
    APIService.makeBooking({
      date: currentDate.format("YYYY-MM-DD"),
      user_id: user.id,
      desk_id: openedDesk.id,
      approved_status: false,
    }).then(
      () => {
        handleModalClose();
        getBookings();
        enqueueSnackbar("Desk booked successfully", {
          variant: "success",
        });
        setLoading(false);
      },
      () => {
        enqueueSnackbar(
          "Error occured while booking desk. Please try again later",
          {
            variant: "error",
          }
        );
        setLoading(false);
      }
    );
  };

  return (
    <>
      <TopBar commonAppBar />
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
                  {room.name}
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
                gap: "3px"
              }}
            >
              {[...Array(32)].map((_, index) => {
                let seperate = [8, 9, 10, 11, 20, 21, 22, 23];
                let desk;
                if (seperate.includes(index) && desks.length > currentDesk) {
                  return <Box></Box>;
                } else if (desks.length > currentDesk + 1) {
                  currentDesk++;
                  desk = desks[currentDesk];
                  return (
                    <Paper
                      sx={{
                        transition: "all 0.13s ease-out",
                        "&:hover": desk.booked
                          ? {}
                          : {
                              cursor: "pointer",
                              transform: "scale(1.06)",
                              transition: "all 0.13s ease-in",
                            },
                        border: 2,
                        borderBottomStyle: "solid",
                        backgroundColor: desk.booked ? "rgba(128,128,128, 0.75)" : "white",
                        textAlign: "center",
                        display: "flex",
                        flexDirection: "column",
                        gap: "10px",
                        justifyContent: "center",
                        alignItems: "center",
                        gridGap: "1px",
                      }}
                      onClick={() => handleModalOpen(desk)}
                    >
                      <Typography style={{ minWidth: "100%", fontWeight: 700, fontSize: "1.5em" }}>
                        Desk {desk.number}
                      </Typography>
                      {desk.booked && (
                        <Typography>
                          Desk booked by {desk.booked_user}
                        </Typography>
                      )}
                    </Paper>
                  );
                }
              })}
            </Box>
          </Box>
        )}
        <Modal
          open={modalOpen}
          onClose={handleModalClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              Book Desk
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
              By clicking the button below, you are confirming that you will sit
              at desk {openedDesk.number} on{" "}
              {currentDate && currentDate.format("YYYY-MM-DD")}
            </Typography>
            <br />
            <LoadingButton
              variant="contained"
              loading={loading}
              onClick={bookDesk}
            >
              Book Desk
            </LoadingButton>
          </Box>
        </Modal>
      </Box>
    </>
  );
};

export default DeskBooking;
