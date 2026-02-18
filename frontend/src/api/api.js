import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export async function login(username, password) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  const res = await API.post("/auth/login", formData);
  return res.data;
}

export async function register(username, password) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  const res = await API.post("/auth/register", formData);
  return res.data;
}

export async function getAdminData() {
  const res = await API.get("/security/analyze/admin");
  return res.data;
}

export async function getUserData(username) {
  const res = await API.get(`/security/analyze/user/${username}`);
  return res.data;
}

export async function getAuditChain() {
  const res = await API.get("/audit/chain");
  return res.data;
}

export async function getFileAccessLogs() {
  const res = await API.get("/admin/file-access");
  return res.data;
}

export async function getPendingUsers() {
  const res = await API.get("/admin/pending-users");
  return res.data;
}

export async function approveUser(username, admin, action) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('admin', admin);
  formData.append('action', action);
  const res = await API.post("/admin/approve-user", formData);
  return res.data;
}

export async function revokeAccess(username, admin) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('admin', admin);
  const res = await API.post("/admin/revoke-access", formData);
  return res.data;
}

export async function checkResourceAccess(resource) {
  const res = await API.get(`/microsegment/check/${resource}`);
  return res.data;
}

export async function getUserSessions(username) {
  const res = await API.get(`/admin/user-sessions/${username}`);
  return res.data;
}
