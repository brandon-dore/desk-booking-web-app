import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8000/';

class APIService {
  getUserInfo() {
    return axios.get(API_URL + 'users/me/', { headers: authHeader() });
  }
  getRooms() {
    return axios.get(API_URL + 'rooms', { headers: authHeader() });
  }
  getDesks(roomId) {
    return axios.get(API_URL + 'desks/' + roomId + "?range=[0,25]", { headers: authHeader() });
  }
  getBookings(date, roomId) {
    return axios.get(API_URL + 'bookings/' + date + "/" + roomId, { headers: authHeader() });
  }
  getUser(userId) {
    return axios.get(API_URL + 'users/' + userId, { headers: authHeader() });
  }
  makeBooking(data) {
    console.log(data)
    return axios.post(API_URL + "bookings", data, { headers: authHeader() });
  }
}

export default new APIService();