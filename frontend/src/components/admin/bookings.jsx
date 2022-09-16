import * as React from "react";
import {
  BooleanField,
  Datagrid,
  DateField,
  List,
  ReferenceField,
  TextField,
  BooleanInput,
  DateInput,
  Edit,
  ReferenceInput,
  SelectInput,
  SimpleForm,
  Create,
} from "react-admin";


export const BookingList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <BooleanField source="approved_status" />
      <DateField source="date" />
      <ReferenceField label="Username" source="user_id" reference="users">
        <TextField source="username" />
      </ReferenceField>
      <ReferenceField label="Desk ID" source="desk_id" reference="desks">
        <TextField source="id" />
      </ReferenceField>
    </Datagrid>
  </List>
);

export const BookingEdit = () => (
  <Edit>
    <SimpleForm>
      <BooleanInput source="approved_status" />
      <DateInput source="date" />
      <ReferenceInput source="desk_id" reference="desks">
        <SelectInput optionText="id" />
      </ReferenceInput>
      <ReferenceInput source="user_id" reference="users">
        <SelectInput optionText="id" />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);

export const BookingCreate = () => (
  <Create>
    <SimpleForm>
      <BooleanInput source="approved_status" />
      <DateInput source="date" />
      <ReferenceInput source="desk_id" reference="desks">
        <SelectInput optionText="id" />
      </ReferenceInput>
      <ReferenceInput source="user_id" reference="users">
        <SelectInput optionText="id" />
      </ReferenceInput>
    </SimpleForm>
  </Create>
);
