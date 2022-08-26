// in src/App.js
import * as React from "react";
import { Admin, Resource, fetchUtils } from "react-admin";
import simpleRestDataProvider from "ra-data-simple-rest";
import Dashboard from "./Dashboard";
import { UserList, UserEdit, UserCreate } from "./users";
import { RoomList, RoomEdit, RoomCreate } from "./rooms";
import { BookingList, BookingEdit, BookingCreate } from "./bookings";
import { DeskList, DeskEdit, DeskCreate } from "./desks";
import { transform, isEqual, isObject } from "lodash";
import UserIcon from "@mui/icons-material/Group";
import AssignmentIcon from "@mui/icons-material/Assignment";
import MeetingRoomIcon from "@mui/icons-material/MeetingRoom";
import DesktopWindowsIcon from '@mui/icons-material/DesktopWindows';

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

export const DeskBookingAdmin = () => (
  <Admin basename="/admin" dashboard={Dashboard} dataProvider={dataProvider}>
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
);
