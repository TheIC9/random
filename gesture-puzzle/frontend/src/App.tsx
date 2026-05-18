// frontend/src/App.tsx
// Top-level component. Owns the FSM, camera setup, and game loop.

import { useEffect, useRef, useState, useCallback } from "react";
import type { GameState, PuzzleState, LeaderboardEntry, BoundingBox } from "./types";
import { classifyGestures, classifyTwoHandGestures } from "./utils/gestureDetector";
import {
  captureImage, generatePuzzleState, renderPuzzle,
  getTileIndexAtCursor, swapTiles, isSolved, getElapsedSeconds,
  dataUrlToBase64
} from "./utils/puzzleLogic";
import { submitScore, getLeaderboard, connectLeaderboardSocket } from "./api/client";
import Leaderboard from "./components/Leaderboard";
import HUD from "./components/HUD";
import "./App.css";

// MediaPipe is loaded via CDN script tag in index.html
declare const HandLandmarker: any;
declare const FilesetResolver: any;

const FIST_HOLD_MS = 1500; // ms to hold fist before reset


export default function App() {
  const videoRef     = useRef<HTMLVideoElement>(null);
  const canvasRef    = useRef<HTMLCanvasElement>(null);
  const handDetector = useRef<any>(null);
  const rafId        = useRef<number>(0);

  // ── State ──────────────────────────────────────────────────────────────────
  const [gameState,   setGameState]   = useState<GameState>("SCANNING");
  const [puzzle,      setPuzzle]      = useState<PuzzleState | null>(null);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [playerName,  setPlayerName]  = useState("Player");
  const [solveTime,   setSolveTime]   = useState(0);

  // Mutable refs for values used inside the rAF loop (avoids stale closures)
  const gameStateRef  = useRef<GameState>("SCANNING");
  const puzzleRef     = useRef<PuzzleState | null>(null);
  const frameBBoxRef  = useRef<BoundingBox | null>(null);
  const fistHoldStart = useRef<number | null>(null);
  const dragStart     = useRef<number>(-1);

  // Keep refs in sync with state
  const setGame = (s: GameState) => { gameStateRef.current = s; setGameState(s); };
  const setPuz  = (p: PuzzleState | null) => { puzzleRef.current = p; setPuzzle(p); };

  // ── MediaPipe setup ────────────────────────────────────────────────────────
  useEffect(() => {
    async function initMediaPipe() {
      const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
      );
      handDetector.current = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
            "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
          delegate: "GPU",
        },
        numHands: 2,
        runningMode: "VIDEO",
      });
      await startCamera();
    }
    initMediaPipe();
    return () => cancelAnimationFrame(rafId.current);
  }, []);

  // ── Camera setup ───────────────────────────────────────────────────────────
  async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 1280, height: 720, facingMode: "user" },
    });
    if (!videoRef.current) return;
    videoRef.current.srcObject = stream;
    videoRef.current.onloadedmetadata = () => {
      videoRef.current!.play();
      startGameLoop();
    };
  }

  // ── WebSocket: live leaderboard ────────────────────────────────────────────
  useEffect(() => {
    const disconnect = connectLeaderboardSocket(setLeaderboard);
    getLeaderboard().then(setLeaderboard).catch(console.error);
    return disconnect;
  }, []);

  // ── THE GAME LOOP ──────────────────────────────────────────────────────────
  function startGameLoop() {
    const video  = videoRef.current!;
    const canvas = canvasRef.current!;
    const ctx    = canvas.getContext("2d")!;

    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;

    function loop(timestamp: number) {
      rafId.current = requestAnimationFrame(loop);

      // 1. Mirror video onto canvas
      ctx.save();
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
      ctx.drawImage(video, 0, 0);
      ctx.restore();

      if (!handDetector.current) return;

      // 2. Run hand detection
      const result  = handDetector.current.detectForVideo(video, timestamp);
      const hands   = result.landmarks.map((lm: any[], i: number) => ({
        landmarks:   lm,
        handedness:  result.handedness[i][0].displayName,
      }));

      // 3. Classify gestures
      const gesture = classifyGestures(hands, canvas.width, canvas.height);
      const twoHand = classifyTwoHandGestures(hands, canvas.width, canvas.height);
      const state   = gameStateRef.current;

      // 4. FSM update
      if (state === "SCANNING") {
        handleScanning(ctx, canvas, twoHand, gesture);
      } else if (state === "PLAYING") {
        handlePlaying(ctx, canvas, gesture, timestamp);
      }

      // 5. Fist → reset (works in any non-SCANNING state)
      if (state !== "SCANNING") {
        if (gesture.isFist) {
          if (!fistHoldStart.current) fistHoldStart.current = Date.now();
          if (Date.now() - fistHoldStart.current > FIST_HOLD_MS) triggerReset();
        } else {
          fistHoldStart.current = null;
        }
      }

      // 6. Draw cursor
      drawCursor(ctx, gesture.cursorX, gesture.cursorY, gesture.pinchStrength);
    }

    rafId.current = requestAnimationFrame(loop);
  }

  // ── SCANNING state handler ─────────────────────────────────────────────────
  function handleScanning(
    ctx: CanvasRenderingContext2D,
    canvas: HTMLCanvasElement,
    twoHand: ReturnType<typeof classifyTwoHandGestures>,
    gesture: ReturnType<typeof classifyGestures>
  ) {
    if (twoHand.frameBBox) {
      frameBBoxRef.current = twoHand.frameBBox;
      drawFrameBox(ctx, twoHand.frameBBox);
    }
    if (twoHand.bothPinching && frameBBoxRef.current) {
      handleCapture(canvas, frameBBoxRef.current);
    }
  }

  // ── PLAYING state handler ──────────────────────────────────────────────────
  function handlePlaying(
    ctx: CanvasRenderingContext2D,
    canvas: HTMLCanvasElement,
    gesture: ReturnType<typeof classifyGestures>,
    _timestamp: number
  ) {
    const puz = puzzleRef.current;
    if (!puz) return;

    // Drag start
    if (gesture.isPinch && dragStart.current === -1) {
      const idx = getTileIndexAtCursor(gesture.cursorX, gesture.cursorY, puz);
      if (idx >= 0) {
        dragStart.current = idx;
        setPuz({ ...puz, draggedTileIndex: idx });
      }
    }

    // Drag end (release pinch)
    if (!gesture.isPinch && dragStart.current !== -1) {
      const dropIdx = getTileIndexAtCursor(gesture.cursorX, gesture.cursorY, puz);
      if (dropIdx >= 0 && dropIdx !== dragStart.current) {
        const newPuz = swapTiles(puz, dragStart.current, dropIdx);
        setPuz(newPuz);
        if (isSolved(newPuz.tiles)) handleSolved(newPuz);
      } else {
        setPuz({ ...puz, draggedTileIndex: null });
      }
      dragStart.current = -1;
    }

    // Render tiles
    renderPuzzle(ctx, puz, gesture.cursorX, gesture.cursorY);
  }

  // ── CAPTURE (SCANNING → PLAYING) ──────────────────────────────────────────
  async function handleCapture(canvas: HTMLCanvasElement, bbox: BoundingBox) {
    const video = videoRef.current!;
    const img   = await captureImage(video, bbox, canvas.width);
    const puz   = generatePuzzleState(img, 3, 3, canvas.width, canvas.height);
    setPuz(puz);
    setGame("PLAYING");
    dragStart.current = -1;
  }

  // ── SOLVED ─────────────────────────────────────────────────────────────────
  async function handleSolved(puz: PuzzleState) {
    const elapsed = getElapsedSeconds(puz);
    setSolveTime(elapsed);
    setGame("SOLVED");

    // Submit score to backend
    await submitScore({
      player_name:  playerName,
      time_seconds: elapsed,
      move_count:   puz.moveCount,
    });

    // Transition to leaderboard after 2.5s
    setTimeout(() => setGame("LEADERBOARD"), 2500);
  }

  // ── RESET ──────────────────────────────────────────────────────────────────
  function triggerReset() {
    setPuz(null);
    setGame("SCANNING");
    frameBBoxRef.current = null;
    dragStart.current    = -1;
    fistHoldStart.current = null;
  }

  // ── DRAW HELPERS ────────────────────────────────────────────────────────────
  function drawFrameBox(ctx: CanvasRenderingContext2D, bbox: BoundingBox) {
    ctx.save();
    ctx.strokeStyle = "rgba(255,255,255,0.8)";
    ctx.lineWidth   = 2;
    ctx.setLineDash([10, 6]);
    ctx.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height);
    ctx.restore();
  }

  function drawCursor(
    ctx: CanvasRenderingContext2D,
    x: number, y: number,
    pinchStrength: number
  ) {
    const r = 16 - pinchStrength * 8; // shrinks when pinching
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(255,220,50,${0.6 + pinchStrength * 0.4})`;
    ctx.lineWidth   = 2;
    ctx.stroke();
    ctx.fillStyle   = `rgba(255,220,50,${pinchStrength * 0.3})`;
    ctx.fill();
  }

  // ── RENDER ────────────────────────────────────────────────────────────────
  return (
    <div className="app">
      <video ref={videoRef} playsInline muted className="video-hidden" />
      <canvas ref={canvasRef} className="game-canvas" />
      <HUD
        gameState={gameState}
        puzzle={puzzle}
        solveTime={solveTime}
        playerName={playerName}
        onNameChange={setPlayerName}
      />
      {(gameState === "SOLVED" || gameState === "LEADERBOARD") && (
        <Leaderboard entries={leaderboard} />
      )}
    </div>
  );
}
