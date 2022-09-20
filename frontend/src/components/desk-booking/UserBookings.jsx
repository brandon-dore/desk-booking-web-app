import React, { useEffect, useState } from "react";
import TopBar from "../header/CommonAppBar";
import APIService from "../services/api.service";
import { experimentalStyled as styled } from "@mui/material/styles";
import {
  Box,
  Paper,
  TableCell,
  TableRow,
  TableBody,
  Table,
  TableContainer,
  TableHead
} from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import { useSnackbar } from "notistack";
import { LocalizationProvider, DesktopDatePicker } from "@mui/x-date-pickers";
import { AdapterMoment } from "@mui/x-date-pickers/AdapterMoment";
import moment from "moment";
import DoneIcon from '@mui/icons-material/Done';
import CloseIcon from '@mui/icons-material/Close';
function createData(date, number, roomName, approved) {
  return { date, number, roomName, approved };
}

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

const UserBookings = () => {
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const [user, setUser] = useState(undefined);

  const [rows, setRows] = useState([]);


  useEffect(() => {
    let rooms;
    APIService.getUserInfo().then(
      (response) => {
        setUser(response.data);
      },
      (error) => {
        enqueueSnackbar("Unable to retrive user info", {
          variant: "error",
        });
      }
    );
    APIService.getRooms().then(
      (response) => {
        rooms = response.data
      },
      (error) => {
        enqueueSnackbar("Unable to retrive rooms", {
          variant: "error",
        });
      }
    )
    APIService.getUserBookings().then(
      (response) => {
        updateTable(response.data, rooms)
      },
      (error) => {
        enqueueSnackbar("Unable to retrive bookings", {
          variant: "error",
        });
      }
    );
  }, []);

  const updateTable = (bookings, rooms) => {
    setRows([])
    bookings.forEach((booking, index) => {
      const room_name = rooms.find(x => x.id === booking.desk.room_id).name;
      setRows(current => [...current, createData(booking.date, booking.desk.number, room_name, booking.approved)])
    }) 
  };

  return (
    <>
      <TopBar commonAppBar />
      <Box sx={{ m: 1, pt: 1, flexGrow: 1 }}>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell align="right">Desk Number</TableCell>
                <TableCell align="right">Room Name</TableCell>
                <TableCell align="right">Approved</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => (
                <TableRow
                  key={row.date}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row.date}
                  </TableCell>
                  <TableCell align="right">{row.number}</TableCell>
                  <TableCell align="right">{row.roomName}</TableCell>
                  <TableCell align="right">{row.approved ? <DoneIcon/>:<CloseIcon/>}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </>
  );
};

export default UserBookings;
