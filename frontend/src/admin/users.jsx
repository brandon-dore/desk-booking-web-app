import * as React from "react";
import {
  Datagrid,
  EmailField,
  List,
  TextField,
  BooleanField,
  BooleanInput,
  Edit,
  SimpleForm,
  TextInput,
  Create,
  PasswordInput,
} from "react-admin";

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

export const UserEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput source="username" />
      <TextInput source="email" />
      <BooleanInput source="admin" />
    </SimpleForm>
  </Edit>
);

export const UserCreate = () => (
    <Create>
      <SimpleForm>
        <TextInput source="username" />
        <TextInput source="email" />
        <BooleanInput source="admin" />
        <PasswordInput source="password" />
      </SimpleForm>
    </Create>
  );
  