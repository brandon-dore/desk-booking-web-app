// in src/Dashboard.js
import * as React from "react";
import { Card, CardContent, CardHeader } from '@mui/material';

const Dashboard = () => (
    <Card>
        <CardHeader title="Welcome to the administration dashboard" />
        <CardContent>This can be used to view the database in a GUI and perform all CRUD operations on each table. To edit a entry simply click on it, make the edits and hit save.</CardContent>
    </Card>
);

export default Dashboard;