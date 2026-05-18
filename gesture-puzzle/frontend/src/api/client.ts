// frontend/src/api/client.ts
// All communication with the Python Flask backend lives here.
// Uses Socket.IO (not raw WebSocket) to match Flask-SocketIO on the backend.

import { io, Socket } from "socket.io-client";
import type {
  ScoreCreate, ScoreOut, LeaderboardEntry,
  ImageProcessRequest, ImageProcessResponse,
} from "../types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";


// ── REST ──────────────────────────────────────────────────────────────────────

/**
 * Submit a solved puzzle score to the backend.
 * Backend persists it and broadcasts a leaderboard update via WebSocket.
 */
export async function submitScore(payload: ScoreCreate): Promise<ScoreOut> {
  const res = await fetch(`${BASE_URL}/api/scores`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`submitScore failed: ${res.status}`);
  return res.json();
}

/**
 * Fetch the current leaderboard (top 10 by solve time).
 */
export async function getLeaderboard(): Promise<LeaderboardEntry[]> {
  const res = await fetch(`${BASE_URL}/api/scores`);
  if (!res.ok) throw new Error(`getLeaderboard failed: ${res.status}`);
  return res.json();
}

/**
 * Optional: send captured image to Python for server-side OpenCV processing.
 * Returns the processed image as base64.
 *
 * Usage:
 *   const result = await processImage({ image_base64: b64, effect: "edge" });
 *   img.src = `data:image/jpeg;base64,${result.image_base64}`;
 */
export async function processImage(
  payload: ImageProcessRequest
): Promise<ImageProcessResponse> {
  const res = await fetch(`${BASE_URL}/api/process-image`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`processImage failed: ${res.status}`);
  return res.json();
}


// ── SOCKET.IO — live leaderboard ──────────────────────────────────────────────

/**
 * Connect to the Flask-SocketIO server.
 * Listens for "leaderboard_update" events and calls onUpdate with fresh data.
 * Returns a cleanup function — call it on component unmount.
 *
 * Usage:
 *   const disconnect = connectLeaderboardSocket((entries) => setLeaderboard(entries));
 *   // On cleanup:
 *   disconnect();
 */
export function connectLeaderboardSocket(
  onUpdate: (entries: LeaderboardEntry[]) => void,
  onError?: (err: Error) => void
): () => void {
  const socket: Socket = io(BASE_URL, {
    transports: ["websocket", "polling"],  // try WebSocket first, fall back to polling
  });

  socket.on("connect", () => {
    console.log("[SocketIO] Connected:", socket.id);
  });

  // This event name matches socketio.emit("leaderboard_update", ...) in Flask
  socket.on("leaderboard_update", (payload: { data: LeaderboardEntry[] }) => {
    onUpdate(payload.data);
  });

  socket.on("connect_error", (err: Error) => {
    console.error("[SocketIO] Connection error:", err.message);
    onError?.(err);
  });

  socket.on("disconnect", (reason: string) => {
    console.log("[SocketIO] Disconnected:", reason);
  });

  // Return cleanup function
  return () => socket.disconnect();
}
