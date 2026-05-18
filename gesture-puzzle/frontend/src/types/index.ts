// frontend/src/types/index.ts
// These mirror the Pydantic schemas in backend/schemas.py exactly.
// Keep these in sync — or auto-generate with:
//   npx openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts

export type GameState = "SCANNING" | "PLAYING" | "SOLVED" | "LEADERBOARD";

// ── API Types ─────────────────────────────────────────────────────────────────

export interface ScoreCreate {
  player_name: string;
  time_seconds: number;
  move_count: number;
  puzzle_image?: string; // base64 JPEG (optional)
}

export interface ScoreOut {
  id: number;
  player_name: string;
  time_seconds: number;
  move_count: number;
  created_at: string; // ISO datetime string
}

export interface LeaderboardEntry extends ScoreOut {
  rank: number;
}

export interface ImageProcessRequest {
  image_base64: string;
  effect: "none" | "blur" | "edge" | "gray";
}

export interface ImageProcessResponse {
  image_base64: string;
}

// ── Game Types ────────────────────────────────────────────────────────────────

export interface Tile {
  id: number;          // original flat index (0-8 for 3×3). NEVER changes.
  origX: number;       // pixel offset in source image (for drawImage crop)
  origY: number;
  currentIndex: number; // current position in the grid array. Changes on swap.
}

export interface Landmark {
  x: number; // normalized 0-1 (raw from MediaPipe — NOT yet screen-flipped)
  y: number;
  z: number;
}

export interface HandData {
  landmarks: Landmark[];
  handedness: "Left" | "Right";
}

export interface GestureResult {
  isPinch: boolean;
  isFrame: boolean;
  isFist: boolean;
  cursorX: number; // smoothed screen X (already flipped)
  cursorY: number; // smoothed screen Y
  pinchStrength: number; // 0-1, for visual feedback
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface PuzzleState {
  tiles: Tile[];
  capturedImage: HTMLImageElement | null;
  tileWidth: number;
  tileHeight: number;
  cols: number;
  rows: number;
  draggedTileIndex: number | null; // index in tiles[] of dragged tile
  moveCount: number;
  startTime: number | null;
}

// ── WebSocket / Socket.IO Events ──────────────────────────────────────────────

// Payload received from Flask-SocketIO "leaderboard_update" event
export interface LeaderboardUpdatePayload {
  data: LeaderboardEntry[];
}
