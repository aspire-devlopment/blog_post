import {jwtDecode} from "jwt-decode";

interface JwtPayload { exp: number; iat: number; user_id: number }

export function isTokenValid(): boolean {
  const token = localStorage.getItem("token");
  if (!token) return false;
  try {
    const payload: JwtPayload = jwtDecode(token);
    return payload.exp > Date.now() / 1000;
  } catch { return false; }
}

export function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}
