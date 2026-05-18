// frontend/src/components/HUD.tsx
// Heads-up display: shows instructions, timer, move count based on game state.

import type { GameState, PuzzleState } from "../types";
import { getElapsedSeconds } from "../utils/puzzleLogic";
import { useEffect, useState } from "react";

interface Props {
  gameState:    GameState;
  puzzle:       PuzzleState | null;
  solveTime:    number;
  playerName:   string;
  onNameChange: (name: string) => void;
}

export default function HUD({ gameState, puzzle, solveTime, playerName, onNameChange }: Props) {
  const [elapsed, setElapsed] = useState(0);

  // Tick the timer while playing
  useEffect(() => {
    if (gameState !== "PLAYING") return;
    const id = setInterval(() => {
      setElapsed(puzzle ? getElapsedSeconds(puzzle) : 0);
    }, 100);
    return () => clearInterval(id);
  }, [gameState, puzzle]);

  return (
    <div className="hud">
      {gameState === "SCANNING" && (
        <div className="hud-panel">
          <p className="hud-instruction">
            Frame a scene with both hands, then pinch to capture
          </p>
          <label className="hud-label">
            Name:
            <input
              className="hud-input"
              value={playerName}
              onChange={e => onNameChange(e.target.value)}
              maxLength={32}
            />
          </label>
        </div>
      )}

      {gameState === "PLAYING" && (
        <div className="hud-panel hud-top-right">
          <span className="hud-timer">{elapsed.toFixed(1)}s</span>
          <span className="hud-moves">Moves: {puzzle?.moveCount ?? 0}</span>
          <span className="hud-hint">Pinch + drag to swap · Fist 1.5s to reset</span>
        </div>
      )}

      {gameState === "SOLVED" && (
        <div className="hud-panel hud-center">
          <h2 className="hud-solved">Solved!</h2>
          <p>{solveTime.toFixed(2)}s · {puzzle?.moveCount} moves</p>
        </div>
      )}

      {gameState === "LEADERBOARD" && (
        <div className="hud-panel hud-hint-bottom">
          <span>Fist for 1.5s to play again</span>
        </div>
      )}
    </div>
  );
}


// ─────────────────────────────────────────────────────────────────────────────
// frontend/src/components/Leaderboard.tsx

import type { LeaderboardEntry } from "../types";

interface LeaderboardProps {
  entries: LeaderboardEntry[];
}

export function Leaderboard({ entries }: LeaderboardProps) {
  return (
    <div className="leaderboard">
      <h3 className="leaderboard-title">Leaderboard</h3>
      {entries.length === 0 && <p className="leaderboard-empty">No scores yet</p>}
      <ol className="leaderboard-list">
        {entries.map(e => (
          <li key={e.id} className="leaderboard-entry">
            <span className="lb-rank">#{e.rank}</span>
            <span className="lb-name">{e.player_name}</span>
            <span className="lb-time">{e.time_seconds.toFixed(2)}s</span>
            <span className="lb-moves">{e.move_count} moves</span>
          </li>
        ))}
      </ol>
    </div>
  );
}

export default Leaderboard;
