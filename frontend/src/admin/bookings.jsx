import * as React from "react";
import { BooleanField, Datagrid, DateField, List, ReferenceField, TextField } from 'react-admin';

export const BookingList = () => (
    <List>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <BooleanField source="approved_status" />
            <DateField source="date" />
            <ReferenceField source="user_id" reference="users">
                <TextField source="username" />
            </ReferenceField>
            <ReferenceField source="desk_id" reference="desks">
                <TextField source="number" />
            </ReferenceField>
        </Datagrid>
    </List>
);