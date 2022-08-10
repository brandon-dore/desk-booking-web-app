import * as React from "react";
import { Datagrid, List, NumberField, TextField } from 'react-admin';

export const DeskList = () => (
    <List>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <NumberField source="number" />
            <TextField source="room" />
            <TextField source="assigned_team" />
        </Datagrid>
    </List>
);