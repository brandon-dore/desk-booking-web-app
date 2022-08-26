import axios from "axios";
import * as qs from "qs";
import jwt_decode from "jwt-decode";

const API_URL = "http://localhost:8000/";
class AuthService {
  login(formValues) {
    return axios
      .post(API_URL + "login", qs.stringify(formValues))
      .then((response) => {
        if (response.data.access_token) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }
        return response.data;
      });
  }
  logout() {
    localStorage.removeItem("user");
  }
  register(formValues) {
    return axios.post(API_URL + "register", formValues);
  }
  getCurrentUser() {
    return JSON.parse(localStorage.getItem("user"));
  }
  getCurrentUsername() {
    const user = this.getCurrentUser();
    if (user) {
      return jwt_decode(user.access_token).sub;
    }
  }
}
export default new AuthService();
