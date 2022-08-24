// in src/App.js
import * as React from "react";
import { Admin, Resource } from 'react-admin';
import jsonServerProvider from 'ra-data-json-server';
import { UserList } from './users';
import { RoomList } from './rooms';
import { BookingList } from './bookings';
import { DeskList } from './desks';

const dataProvider = jsonServerProvider('http://localhost:8000');

export const DeskBookingAdmin = () => (
    <Admin basename="/admin" dataProvider={dataProvider}>
        <Resource name="users" list={UserList} />
        <Resource name="bookings" list={BookingList} />
        <Resource name="rooms" list={RoomList} />
        <Resource name="desks" list={DeskList} />
    </Admin>
);