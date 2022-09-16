import * as React from "react";
import {
  Datagrid,
  List,
  NumberField,
  TextField,
  ReferenceField,
  Edit,
  NumberInput,
  ReferenceInput,
  SelectInput,
  SimpleForm,
  Create
} from "react-admin";

export const DeskList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <NumberField source="number" />
      <ReferenceField source="room_id" reference="rooms">
        <TextField source="name" />
      </ReferenceField>
    </Datagrid>
  </List>
);

export const DeskEdit = () => (
  <Edit>
    <SimpleForm>
      <NumberInput source="number" />
      <ReferenceInput source="room_id" reference="rooms">
        <SelectInput optionText="id" />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);

export const DeskCreate = () => (
  <Create>
    <SimpleForm>
      <NumberInput source="number" />
      <ReferenceInput source="room_id" reference="rooms">
        <SelectInput optionText="id" />
      </ReferenceInput>
    </SimpleForm>
  </Create>
);
