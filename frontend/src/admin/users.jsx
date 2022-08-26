import * as React from "react";
import { Datagrid, EmailField, List, TextField, BooleanField } from 'react-admin';

export const UserList = () => (
    <List>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="username" />
            <EmailField source="email" />
            <BooleanField source="admin" />
        </Datagrid>
    </List>
);
