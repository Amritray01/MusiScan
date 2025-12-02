// frontend/src/api/index.js
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
});

export function setAuthToken(token){
  if(token) api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  else delete api.defaults.headers.common["Authorization"];
}

/* User / songs */
export const fetchSongs = (params={}) => api.get("/user/songs", { params }).then(r => r.data);
export const searchSongs = (q) => api.get("/user/search", { params: { q } }).then(r => r.data);
export const autocomplete = (q) => api.get("/user/autocomplete", { params: { q } }).then(r => r.data);

/* Favorites (auth required) */
export const addFavorite = (payload) => api.post("/user/favorite", payload).then(r=>r.data);
export const getFavorites = () => api.get("/user/favorites").then(r=>r.data);
export const removeFavorite = ({ item_type, item_value }) => api.delete("/user/favorite", { params: { item_type, item_value } }).then(r=>r.data);

/* Alerts */
export const getAlerts = () => api.get("/user/alerts").then(r=>r.data);

/* Admin (auth required) */
export const adminAddSong = (payload) => api.post("/admin/song", payload).then(r=>r.data);
export const adminAddArtist = (payload) => api.post("/admin/artist", payload).then(r=>r.data);
export const adminAddAlbum = (payload) => api.post("/admin/album", payload).then(r=>r.data);

export default api;
