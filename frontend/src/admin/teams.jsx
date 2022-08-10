import * as React from "react";
import { Datagrid, List, TextField } from 'react-admin';

export const TeamList = () => (
    <List>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="name" />
        </Datagrid>
    </List>
);