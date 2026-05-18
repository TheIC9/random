// frontend/src/utils/puzzleLogic.ts
// All pure puzzle logic — no DOM, no canvas, no gestures.

import type { Tile, PuzzleState, BoundingBox } from "../types";

const DEFAULT_COLS = 3;
const DEFAULT_ROWS = 3;


// ── PUZZLE GENERATION ─────────────────────────────────────────────────────────

/**
 * Capture a region of the video element to an offscreen canvas,
 * returning it as an HTMLImageElement ready for use with drawImage().
 *
 * @param video   The live <video> element
 * @param bbox    The bounding box (from hand frame gesture) in canvas pixels
 * @param displayW  Canvas display width (for mirroring)
 */
export async function captureImage(
  video: HTMLVideoElement,
  bbox: BoundingBox,
  displayW: number
): Promise<HTMLImageElement> {
  const offscreen = document.createElement("canvas");
  offscreen.width  = bbox.width;
  offscreen.height = bbox.height;
  const ctx = offscreen.getContext("2d")!;

  // Mirror the video (flip horizontally) before cropping
  ctx.translate(bbox.width, 0);
  ctx.scale(-1, 1);

  // Draw just the bounding box region from the video frame
  // Source coords must be UNFLIPPED (video's own coordinate space)
  const srcX = displayW - bbox.x - bbox.width; // un-flip X for source
  ctx.drawImage(
    video,
    srcX, bbox.y, bbox.width, bbox.height, // source crop (video space)
    0,    0,      bbox.width, bbox.height  // dest (full offscreen canvas)
  );

  // Convert canvas → data URL → HTMLImageElement
  const dataURL = offscreen.toDataURL("image/jpeg", 0.9);
  return loadImage(dataURL);
}

/**
 * Build initial puzzle state from a captured image.
 * Tiles are Fisher-Yates shuffled.
 */
export function generatePuzzleState(
  capturedImage: HTMLImageElement,
  cols = DEFAULT_COLS,
  rows = DEFAULT_ROWS,
  canvasW: number,
  canvasH: number
): PuzzleState {
  const tileWidth  = Math.floor(canvasW / cols);
  const tileHeight = Math.floor(canvasH / rows);

  // Build ordered tiles
  const tiles: Tile[] = Array.from({ length: cols * rows }, (_, i) => ({
    id:           i,
    origX:        (i % cols) * tileWidth,
    origY:        Math.floor(i / cols) * tileHeight,
    currentIndex: i,
  }));

  // Shuffle — Fisher-Yates
  fisherYates(tiles);

  // Update currentIndex to reflect shuffled positions
  tiles.forEach((tile, idx) => { tile.currentIndex = idx; });

  return {
    tiles,
    capturedImage,
    tileWidth,
    tileHeight,
    cols,
    rows,
    draggedTileIndex: null,
    moveCount: 0,
    startTime: Date.now(),
  };
}


// ── TILE INTERACTION ──────────────────────────────────────────────────────────

/**
 * Find which tile (array index) the cursor is hovering over.
 * Returns -1 if cursor is outside the grid.
 */
export function getTileIndexAtCursor(
  cursorX: number,
  cursorY: number,
  state: PuzzleState
): number {
  const col = Math.floor(cursorX / state.tileWidth);
  const row = Math.floor(cursorY / state.tileHeight);
  if (col < 0 || col >= state.cols || row < 0 || row >= state.rows) return -1;
  return row * state.cols + col;
}

/**
 * Swap two tiles by their array indices. Mutates state.tiles.
 * Returns the new state (immutable-style clone).
 */
export function swapTiles(state: PuzzleState, indexA: number, indexB: number): PuzzleState {
  if (indexA === indexB) return state;
  const tiles = [...state.tiles];
  [tiles[indexA], tiles[indexB]] = [tiles[indexB], tiles[indexA]];
  tiles[indexA].currentIndex = indexA;
  tiles[indexB].currentIndex = indexB;
  return { ...state, tiles, moveCount: state.moveCount + 1, draggedTileIndex: null };
}


// ── WIN DETECTION ─────────────────────────────────────────────────────────────

/**
 * A puzzle is solved when every tile's original id equals its current index.
 * tiles[0].id === 0, tiles[1].id === 1, ... tiles[8].id === 8
 */
export function isSolved(tiles: Tile[]): boolean {
  return tiles.every((tile, index) => tile.id === index);
}

/**
 * Elapsed time in seconds since puzzle start.
 */
export function getElapsedSeconds(state: PuzzleState): number {
  if (!state.startTime) return 0;
  return (Date.now() - state.startTime) / 1000;
}


// ── CANVAS RENDERING ──────────────────────────────────────────────────────────

/**
 * Draw the puzzle grid onto a canvas context.
 * Called every frame during PLAYING state.
 *
 * @param ctx        Canvas 2D rendering context
 * @param state      Current puzzle state
 * @param dragCursorX  Current cursor X (for drawing dragged tile)
 * @param dragCursorY  Current cursor Y
 */
export function renderPuzzle(
  ctx: CanvasRenderingContext2D,
  state: PuzzleState,
  dragCursorX: number,
  dragCursorY: number
) {
  const { tiles, capturedImage, tileWidth, tileHeight, cols, draggedTileIndex } = state;
  if (!capturedImage) return;

  tiles.forEach((tile, index) => {
    if (index === draggedTileIndex) return; // draw dragged tile last (on top)

    const destCol = index % cols;
    const destRow = Math.floor(index / cols);
    const destX   = destCol * tileWidth;
    const destY   = destRow * tileHeight;

    // Slice the correct region from the captured image
    ctx.drawImage(
      capturedImage,
      tile.origX, tile.origY, tileWidth, tileHeight, // source crop
      destX,      destY,      tileWidth, tileHeight  // dest position
    );

    // Tile border
    ctx.strokeStyle = "rgba(255,255,255,0.4)";
    ctx.lineWidth = 1;
    ctx.strokeRect(destX, destY, tileWidth, tileHeight);
  });

  // Draw dragged tile floating at cursor
  if (draggedTileIndex !== null && draggedTileIndex >= 0) {
    const draggedTile = tiles[draggedTileIndex];
    ctx.globalAlpha = 0.85;
    ctx.drawImage(
      capturedImage,
      draggedTile.origX, draggedTile.origY, tileWidth, tileHeight,
      dragCursorX - tileWidth  / 2,
      dragCursorY - tileHeight / 2,
      tileWidth, tileHeight
    );
    ctx.globalAlpha = 1.0;

    // Highlight border on dragged tile
    ctx.strokeStyle = "rgba(255,220,50,0.9)";
    ctx.lineWidth = 3;
    ctx.strokeRect(
      dragCursorX - tileWidth  / 2,
      dragCursorY - tileHeight / 2,
      tileWidth, tileHeight
    );
  }
}


// ── PRIVATE UTILITIES ─────────────────────────────────────────────────────────

/**
 * Fisher-Yates in-place shuffle. O(n), unbiased.
 */
function fisherYates<T>(arr: T[]): void {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

/**
 * Load a data URL into an HTMLImageElement.
 */
function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload  = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}

/**
 * Extract base64 string from a data URL (strips the "data:image/jpeg;base64," prefix).
 */
export function dataUrlToBase64(dataUrl: string): string {
  return dataUrl.split(",")[1] ?? "";
}
