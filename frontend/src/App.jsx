import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home } from './desk-booking/Home';
import { DeskBookingAdmin } from './admin/DeskBookingAdmin';

const App = () => (
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/admin/*" element={<DeskBookingAdmin />} />
        </Routes>
    </BrowserRouter>
);

export default App