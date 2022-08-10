import * as React from "react";
import { Datagrid, List, TextField } from 'react-admin';

export const RoomList = () => (
    <List>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="name" />
        </Datagrid>
    </List>
);