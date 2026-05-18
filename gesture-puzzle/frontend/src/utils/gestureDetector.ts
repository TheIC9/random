// frontend/src/utils/gestureDetector.ts
// Pure geometry — no ML. Converts MediaPipe landmarks into game gestures.

import type { Landmark, HandData, GestureResult, BoundingBox } from "../types";

// ── Constants ─────────────────────────────────────────────────────────────────
const PINCH_THRESHOLD = 0.05;   // normalized dist between thumb+index tips
const FRAME_THRESHOLD = 0.10;   // hand is "open" for framing
const EMA_ALPHA       = 0.4;    // smoothing factor (0=frozen, 1=raw)
const EMA_JUMP_PX     = 100;    // skip smoothing if cursor jumps this far

// Landmark indices (MediaPipe 21-point hand model)
const THUMB_TIP   = 4;
const INDEX_TIP   = 8;
const MIDDLE_TIP  = 12;
const RING_TIP    = 16;
const PINKY_TIP   = 20;
const INDEX_PIP   = 6;  // proximal interphalangeal — middle knuckle
const MIDDLE_PIP  = 10;
const RING_PIP    = 14;
const PINKY_PIP   = 18;
const WRIST       = 0;

// ── Smoothed cursor state (module-level — persists across frames) ─────────────
let smoothedX = 0;
let smoothedY = 0;


// ── PUBLIC API ────────────────────────────────────────────────────────────────

/**
 * Given raw landmark data from MediaPipe, return gesture state.
 * @param hands  Array of detected hands (0, 1, or 2 hands)
 * @param canvasW  Canvas width in CSS pixels (for coordinate conversion)
 * @param canvasH  Canvas height in CSS pixels
 */
export function classifyGestures(
  hands: HandData[],
  canvasW: number,
  canvasH: number
): GestureResult {
  if (hands.length === 0) {
    return { isPinch: false, isFrame: false, isFist: false,
             cursorX: smoothedX, cursorY: smoothedY, pinchStrength: 0 };
  }

  const hand = hands[0]; // primary hand (use hands[1] for two-hand gestures)
  const lm   = hand.landmarks;

  const pinchDist = euclidean(lm[THUMB_TIP], lm[INDEX_TIP]);
  const isPinch   = pinchDist < PINCH_THRESHOLD;
  const isFrame   = pinchDist > FRAME_THRESHOLD;
  const isFist    = detectFist(lm);

  // Pinch strength: 0 = fully open, 1 = fully pinched
  const pinchStrength = 1 - Math.min(pinchDist / FRAME_THRESHOLD, 1);

  // Cursor = midpoint of thumb and index tips, screen-converted + smoothed
  const rawX = flipX(midpoint(lm[THUMB_TIP].x, lm[INDEX_TIP].x)) * canvasW;
  const rawY = midpoint(lm[THUMB_TIP].y, lm[INDEX_TIP].y) * canvasH;

  applyCursorSmoothing(rawX, rawY, canvasW, canvasH);

  return {
    isPinch,
    isFrame,
    isFist,
    cursorX: smoothedX,
    cursorY: smoothedY,
    pinchStrength,
  };
}

/**
 * For two-hand SCANNING mode: detect simultaneous pinch on both hands,
 * and compute the bounding box their fingertips define.
 */
export function classifyTwoHandGestures(
  hands: HandData[],
  canvasW: number,
  canvasH: number
): { bothPinching: boolean; frameBBox: BoundingBox | null } {
  if (hands.length < 2) return { bothPinching: false, frameBBox: null };

  const [h1, h2] = hands;
  const pinch1 = euclidean(h1.landmarks[THUMB_TIP], h1.landmarks[INDEX_TIP]) < PINCH_THRESHOLD;
  const pinch2 = euclidean(h2.landmarks[THUMB_TIP], h2.landmarks[INDEX_TIP]) < PINCH_THRESHOLD;
  const bothPinching = pinch1 && pinch2;

  // Build bounding box from all 4 fingertip pairs
  const tips = [
    h1.landmarks[THUMB_TIP], h1.landmarks[INDEX_TIP],
    h2.landmarks[THUMB_TIP], h2.landmarks[INDEX_TIP],
  ];

  const xs = tips.map(p => flipX(p.x) * canvasW);
  const ys = tips.map(p => p.y * canvasH);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);

  const frameBBox: BoundingBox = {
    x: minX, y: minY,
    width:  maxX - minX,
    height: maxY - minY,
  };

  return { bothPinching, frameBBox };
}

/**
 * Reset cursor smoothing state (call when hand re-enters frame).
 */
export function resetCursorSmoothing(x = 0, y = 0) {
  smoothedX = x;
  smoothedY = y;
}


// ── PRIVATE HELPERS ───────────────────────────────────────────────────────────

/**
 * Euclidean distance in normalized (0-1) landmark space.
 * Scale-invariant: same threshold works at any hand distance from camera.
 */
function euclidean(a: Landmark, b: Landmark): number {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

/**
 * Fist: all 4 finger tips are CLOSER to the wrist than their PIP joints.
 * This is a simple geometric rule — no ML classifier needed.
 */
function detectFist(lm: Landmark[]): boolean {
  const fingerPairs = [
    [INDEX_TIP, INDEX_PIP],
    [MIDDLE_TIP, MIDDLE_PIP],
    [RING_TIP, RING_PIP],
    [PINKY_TIP, PINKY_PIP],
  ];
  return fingerPairs.every(([tip, pip]) => {
    const tipToWrist = euclidean(lm[tip],  lm[WRIST]);
    const pipToWrist = euclidean(lm[pip],  lm[WRIST]);
    return tipToWrist < pipToWrist; // tip is closer to wrist → finger is curled
  });
}

/**
 * MediaPipe x=0 is the camera's right edge.
 * Since the video is displayed mirrored, flip x so 0 = left on screen.
 */
function flipX(x: number): number {
  return 1 - x;
}

function midpoint(a: number, b: number): number {
  return (a + b) / 2;
}

/**
 * Exponential moving average for the cursor.
 * Jumps to raw immediately if movement > EMA_JUMP_PX (avoids lag on fast moves).
 */
function applyCursorSmoothing(rawX: number, rawY: number, _cW: number, _cH: number) {
  const delta = Math.hypot(rawX - smoothedX, rawY - smoothedY);
  const alpha = delta > EMA_JUMP_PX ? 1.0 : EMA_ALPHA;
  smoothedX = alpha * rawX + (1 - alpha) * smoothedX;
  smoothedY = alpha * rawY + (1 - alpha) * smoothedY;
}
