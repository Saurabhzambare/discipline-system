
import { useEffect, useState } from "react";

export default function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/health/")
      .then((r) => r.json())
      .then(setHealth)
      .catch((e) => setHealth({ status: "error", message: String(e) }));
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-6">
      <div className="w-full max-w-xl rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold tracking-wide">
            DISCIPLINE SYSTEM
          </h1>
          <span className="text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-200">
            Phase 0
          </span>
        </div>

        <p className="mt-3 text-slate-300">
          Player Status Window (Prototype)
        </p>

        <div className="mt-6 grid grid-cols-3 gap-3">
          <div className="rounded-xl border border-slate-800 p-3">
            <p className="text-xs text-slate-400">LEVEL</p>
            <p className="text-lg font-bold">1</p>
          </div>
          <div className="rounded-xl border border-slate-800 p-3">
            <p className="text-xs text-slate-400">EXP</p>
            <p className="text-lg font-bold">0 / 100</p>
          </div>
          <div className="rounded-xl border border-slate-800 p-3">
            <p className="text-xs text-slate-400">STREAK</p>
            <p className="text-lg font-bold">0</p>
          </div>
        </div>

        <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950/60 p-4">
          <p className="text-sm text-slate-400">API Health Check</p>
          <pre className="mt-2 text-sm overflow-auto">
            {health ? JSON.stringify(health, null, 2) : "Loading..."}
          </pre>
        </div>
      </div>
    </div>
  );
}

// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'


// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vite.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.jsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// export default App
