import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api"; // URL du backend FastAPI

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
