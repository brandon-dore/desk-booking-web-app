import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8000/';

// Reusable methods to call the API, excluding auth
class APIService {
  getUserInfo() {
    return axios.get(API_URL + 'users/me/', { headers: authHeader() });
  }
  getUserBookings() {
    return axios.get(API_URL + 'users/me/bookings/', { headers: authHeader() });
  }
  getRooms() {
    return axios.get(API_URL + 'rooms', { headers: authHeader() });
  }
  getDesks(roomId) {
    return axios.get(API_URL + 'rooms/' + roomId + '/desks' +  '?range=[0,25]', { headers: authHeader() });
  }
  getBookings(date, roomId) {
    return axios.get(API_URL + 'rooms/' + roomId + "/bookings/" + date, { headers: authHeader() });
  }
  getUser(userId) {
    return axios.get(API_URL + 'users/' + userId, { headers: authHeader() });
  }
  makeBooking(data) {
    return axios.post(API_URL + "bookings", data, { headers: authHeader() });
  }
}

export default new APIService();