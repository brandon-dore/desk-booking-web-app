// in src/App.js
import React, { useEffect, useState } from "react";

import { transform, isEqual, isObject } from "lodash";
import {
  Container,
  Box,
  CssBaseline,
  Typography,
} from "@mui/material";
import UserIcon from "@mui/icons-material/Group";
import AssignmentIcon from "@mui/icons-material/Assignment";
import MeetingRoomIcon from "@mui/icons-material/MeetingRoom";
import DesktopWindowsIcon from "@mui/icons-material/DesktopWindows";
import simpleRestDataProvider from "ra-data-simple-rest";

import { Admin, Resource, fetchUtils, Layout  } from "react-admin";
import { UserList, UserEdit, UserCreate } from "./users";
import { RoomList, RoomEdit, RoomCreate } from "./rooms";
import { BookingList, BookingEdit, BookingCreate } from "./bookings";
import { DeskList, DeskEdit, DeskCreate } from "./desks";
import Dashboard from "./Dashboard";
import APIService from "../services/api.service";
import TopBar from "../header/CommonAppBar";

const httpClient = fetchUtils.fetchJson;

const baseDataProvider = simpleRestDataProvider("http://localhost:8000");

const diff = (object, base) => {
  return transform(object, (result, value, key) => {
    if (!isEqual(value, base[key])) {
      result[key] =
        isObject(value) && isObject(base[key]) ? diff(value, base[key]) : value;
    }
  });
};

export const dataProvider = {
  ...baseDataProvider,
  update: (resource, params) =>
    httpClient(`http://localhost:8000/${resource}/${params.id}`, {
      method: "PATCH",
      body: JSON.stringify(diff(params.data, params.previousData)),
    }).then(({ json }) => ({ data: json })),
};

const MyLayout = (props) => <Layout {...props} appBar={TopBar} />;

export const DeskBookingAdmin = () => {
  const [isAdmin, setIsAdmin] = useState(undefined);

  useEffect(() => {
    APIService.getUserInfo().then(
      (response) => {
        console.log(response)
        setIsAdmin(response.data.admin);
      },
      (error) => {
        console.log(error);
      }
    );
  }, []);

  return (
    <>
      {!isAdmin && (
        <>
          <TopBar />
          <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box
              sx={{
                marginTop: 8,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                textTransform: "uppercase",
                textAlign: "center",
                fontWeight: "bold",
              }}
            >
              <Typography component="h1" variant="h5">
                You need to be an admin to view this page
              </Typography>
            </Box>
          </Container>
        </>
      )}
      {isAdmin && (
        <Admin
          basename="/admin"
          dashboard={Dashboard}
          dataProvider={dataProvider}
          layout={MyLayout}
        >
          <Resource
            name="users"
            list={UserList}
            edit={UserEdit}
            create={UserCreate}
            icon={UserIcon}
          />
          <Resource
            name="bookings"
            list={BookingList}
            edit={BookingEdit}
            create={BookingCreate}
            icon={AssignmentIcon}
          />
          <Resource
            name="rooms"
            list={RoomList}
            edit={RoomEdit}
            create={RoomCreate}
            icon={MeetingRoomIcon}
          />
          <Resource
            name="desks"
            list={DeskList}
            edit={DeskEdit}
            create={DeskCreate}
            icon={DesktopWindowsIcon}
          />
        </Admin>
      )}
    </>
  );
};
