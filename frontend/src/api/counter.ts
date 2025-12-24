import axios from "axios";

export const api = axios.create({
  baseURL: "/api",
});

export const getCounter = () => api.get("/counter");
export const increment = () => api.post("/counter/increment");
export const decrement = () => api.post("/counter/decrement");
export const reset = () => api.post("/counter/reset");
