import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Play, Pause, RefreshCw, Shield, Hash, Activity, FlaskConical, X, RefreshCcw, Search, Target, Map, Grid3X3, Maximize, BarChart3, Wand2, Crosshair, Microscope, Cpu, Trophy, AlertTriangle } from 'lucide-react';

/**
 * WADA CHAOS RNG (BATTLE ROYALE MODE)
 * * Feature: "Adaptive Weakness Weeding".
 * * Comparison: Runs Wada vs PRNG vs Hybrid on shrinking datasets.
 * * Metric: Scores algorithms based on Entropy and Chi-Squared Deviation.
 * * Goal: Expose which algorithm fails first as sample size drops.
 */

// --- PHYSICS CONSTANTS ---
const DT = 0.05; 
const ESCAPE_R2 = 25.0; 
const MAX_STEPS = 1000; 
const SIGMA = 1.0; 

// --- GRID SETTINGS ---
const GRID_SIZE = 100; 
const UPDATE_BATCH = 2000; 

// --- UTILITIES ---

const BASIN_COLORS = {
  0: '#1f2937', 
  1: '#ef4444', 
  2: '#3b82f6', 
  3: '#10b981', 
};

const fastHash = (n) => {
  n = Math.imul(n, 0x5bd1e995);
  n ^= n >>> 15;
  n = Math.imul(n, 0x27d4eb2d);
  return n >>> 0;
}

const getPixelColor = (stress, basin) => {
  const intensity = Math.min(stress * 2, 255); 
  let r, g, b;
  
  if (basin === 0) { 
     r = intensity * 0.5; g = intensity * 0.2; b = intensity * 0.5;
  } else if (basin === 1) { 
     r = intensity; g = intensity * 0.2; b = intensity * 0.2;
  } else if (basin === 2) { 
     r = intensity * 0.1; g = intensity * 0.5; b = intensity;
  } else { 
     r = intensity * 0.1; g = intensity; b = intensity * 0.3;
  }
  return [Math.floor(r), Math.floor(g), Math.floor(b)];
};

// Advanced Stats
const calculateStats = (data) => {
  if (data.length === 0) return { entropy: 0, chiSq: 0 };
  
  const frequencies = new Array(256).fill(0);
  data.forEach(val => frequencies[val]++);
  
  // Shannon Entropy
  const entropy = frequencies.reduce((sum, count) => {
    if (count === 0) return sum;
    const p = count / data.length;
    return sum - (p * Math.log2(p));
  }, 0);

  // Chi-Squared Test (Uniformity)
  const expected = data.length / 256;
  const chiSq = frequencies.reduce((sum, count) => {
    return sum + ((count - expected) ** 2) / expected;
  }, 0);

  return { entropy, chiSq };
};

export default function WadaChaosRNG() {
  const [entropyPool, setEntropyPool] = useState([]); 
  const [generatedKey, setGeneratedKey] = useState('');
  const [avgFrustration, setAvgFrustration] = useState(0); 
  const [isRunning, setIsRunning] = useState(true);
  const [showLab, setShowLab] = useState(false); 
  const [whitening, setWhitening] = useState(false);
  const [hunting, setHunting] = useState(true); 
  
  // Battle Royale State
  const [sampleSize, setSampleSize] = useState(500); // Adjustable N
  const [autoShrink, setAutoShrink] = useState(false); // Mode to automatically reduce N
  
  const [view, setView] = useState({ x: 0, y: 0, zoom: 1.0 });
  const [controlData, setControlData] = useState([]);
  const [hybridData, setHybridData] = useState([]); 

  const canvasRef = useRef(null);
  const requestRef = useRef(null);
  const gridStressRef = useRef(new Float32Array(GRID_SIZE * GRID_SIZE));
  const gridBasinRef = useRef(new Uint8Array(GRID_SIZE * GRID_SIZE));
  
  const entropyBufferRef = useRef([]);
  const hybridBufferRef = useRef([]); 
  const lastByteRef = useRef(0);

  // --- PHYSICS KERNEL ---
  const computeCell = (m, l) => {
    let pm = 0, pl = 0;
    let steps = 0;
    let stress = 0;
    
    while (steps < MAX_STEPS) {
        const fm = -(m + 2 * SIGMA * m * l);
        const fl = -(l + SIGMA * (m * m - l * l));
        stress += Math.sqrt(fm*fm + fl*fl) * DT;

        pm += 0.5 * DT * fm; pl += 0.5 * DT * fl;
        m += DT * pm; l += DT * pl;
        
        const fm2 = -(m + 2 * SIGMA * m * l);
        const fl2 = -(l + SIGMA * (m * m - l * l));
        pm += 0.5 * DT * fm2; pl += 0.5 * DT * fl2;
        
        if (m*m + l*l > ESCAPE_R2) {
            const angle = Math.atan2(l, m);
            if (angle > 0.5 && angle < 2.6) return { stress, basin: 1 };
            if (angle <= -2.6 || angle >= 2.6) return { stress, basin: 2 };
            return { stress, basin: 3 };
        }
        steps++;
    }
    return { stress, basin: 0 };
  };

  // --- RENDER LOOP ---
  const loop = useCallback(() => {
    if (!canvasRef.current) return;
    const ctx = canvasRef.current.getContext('2d');
    const imgData = ctx.getImageData(0, 0, GRID_SIZE, GRID_SIZE);
    const data = imgData.data;
    
    let maxStressX = 0, maxStressY = 0, maxStressVal = 0, stressSum = 0;
    let frameStressSum = 0, frameUpdates = 0;
    
    for (let i = 0; i < UPDATE_BATCH; i++) {
        const px = Math.floor(Math.random() * GRID_SIZE);
        const py = Math.floor(Math.random() * GRID_SIZE);
        const idx = py * GRID_SIZE + px;
        
        const physicsX = view.x + (px - GRID_SIZE/2) / (20 * view.zoom);
        const physicsY = view.y - (py - GRID_SIZE/2) / (20 * view.zoom);
        
        const result = computeCell(physicsX, physicsY);
        gridStressRef.current[idx] = result.stress;
        gridBasinRef.current[idx] = result.basin;

        if (result.stress > 2.0) { 
            maxStressX += physicsX * result.stress;
            maxStressY += physicsY * result.stress;
            stressSum += result.stress;
            if (result.stress > maxStressVal) maxStressVal = result.stress;
        }
        
        if (result.stress > 1.0) {
             const input = (idx * 1000) + (result.stress * 100) + result.basin;
             let wadaByte = fastHash(Math.floor(input)) % 256;
             
             if (whitening) wadaByte = wadaByte ^ lastByteRef.current;
             lastByteRef.current = wadaByte;

             entropyBufferRef.current.push({ 
                 val: wadaByte, 
                 basin: result.basin, 
                 stress: result.stress 
             });
             
             const prngByte = Math.floor(Math.random() * 256);
             const hybridByte = wadaByte ^ prngByte;
             
             hybridBufferRef.current.push(hybridByte);
        }
        frameStressSum += result.stress;
        frameUpdates++;
    }
    
    if (isRunning && hunting && stressSum > 0) {
        const targetX = maxStressX / stressSum;
        const targetY = maxStressY / stressSum;
        const moveSpeed = 0.05;
        const newX = view.x + (targetX - view.x) * moveSpeed;
        const newY = view.y + (targetY - view.y) * moveSpeed;
        
        const avgS = frameStressSum / frameUpdates;
        let targetZoom = view.zoom;
        if (avgS > 50) targetZoom *= 1.02; 
        else if (avgS < 10) targetZoom *= 0.98;
        targetZoom = Math.max(0.1, Math.min(targetZoom, 100.0));
        
        setView({ x: newX, y: newY, zoom: targetZoom });
    } else if (isRunning && !hunting) {
         setView(v => ({
            x: v.x + (Math.random() - 0.5) * 0.002,
            y: v.y + (Math.random() - 0.5) * 0.002,
            zoom: v.zoom
        }));
    }
    
    // Always keep enough buffer for tests, UI will slice
    if (entropyBufferRef.current.length > 5000) {
        entropyBufferRef.current = entropyBufferRef.current.slice(-5000);
        hybridBufferRef.current = hybridBufferRef.current.slice(-5000);
    }
    
    setEntropyPool([...entropyBufferRef.current]);
    setHybridData([...hybridBufferRef.current]);
    setAvgFrustration(frameStressSum / (frameUpdates || 1));

    for (let i = 0; i < GRID_SIZE * GRID_SIZE; i++) {
        const stress = gridStressRef.current[i];
        const basin = gridBasinRef.current[i];
        const color = getPixelColor(stress, basin);
        const dataIdx = i * 4;
        data[dataIdx] = color[0]; data[dataIdx + 1] = color[1]; 
        data[dataIdx + 2] = color[2]; data[dataIdx + 3] = 255;
    }
    
    ctx.putImageData(imgData, 0, 0);
    requestRef.current = requestAnimationFrame(loop);
  }, [isRunning, view, whitening, hunting]); 

  useEffect(() => {
    requestRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(requestRef.current);
  }, [loop]);

  // --- AUTO SHRINK LOGIC ---
  useEffect(() => {
      if (!autoShrink || !showLab) return;
      
      const interval = setInterval(() => {
          setSampleSize(prev => {
              if (prev <= 10) return 500; // Reset loop
              return Math.max(10, Math.floor(prev * 0.9)); // Shrink by 10%
          });
      }, 500); // Shrink every 0.5s
      
      return () => clearInterval(interval);
  }, [autoShrink, showLab]);

  // --- CONTROL GROUP ---
  useEffect(() => {
    if (!showLab) return;
    const generateControl = () => {
        // Generate massive pool, we will slice in the component
        return Array.from({length: 5000}, () => Math.floor(Math.random() * 256));
    };
    
    // Init
    if(controlData.length === 0) setControlData(generateControl());

    const interval = setInterval(() => {
        setControlData(prev => [...prev.slice(100), ...Array.from({length: 100}, () => Math.floor(Math.random() * 256))]);
    }, 100); 
    return () => clearInterval(interval);
  }, [showLab]);

  const generateLiveKey = useCallback(() => {
    if (entropyPool.length < 8) return "HUNTING...";
    const raw = entropyPool.slice(-50).map(e => e.val.toString(16).padStart(2, '0')).join('');
    const viewHash = Math.floor((view.x + view.y + view.zoom) * 10000).toString(16);
    return (raw + viewHash).substring(0, 32);
  }, [entropyPool, view]);

  useEffect(() => {
    setGeneratedKey(generateLiveKey());
  }, [generateLiveKey]);

  return (
    <div className="flex flex-col md:flex-row h-screen bg-black text-gray-200 font-sans overflow-hidden">
      {/* LEFT PANEL */}
      <div className="relative flex-1 bg-gray-900 border-r border-gray-800 flex flex-col">
        <div className="flex-1 relative overflow-hidden flex items-center justify-center bg-gray-950">
            <canvas
              ref={canvasRef}
              width={GRID_SIZE}
              height={GRID_SIZE}
              className="w-full h-full object-contain rendering-pixelated"
              style={{ imageRendering: 'pixelated' }}
            />
            {hunting && (
                <div className="absolute inset-0 border-2 border-red-500/30 pointer-events-none animate-pulse">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-20 h-20 border border-red-500/50 rounded-full" />
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-1 h-1 bg-red-500" />
                </div>
            )}
            <div className="absolute inset-0 pointer-events-none bg-gradient-to-t from-gray-900 via-transparent to-transparent opacity-50" />
        </div>
        
        <div className="absolute top-4 left-4 p-4 bg-black/70 backdrop-blur-md rounded-xl border border-gray-700 pointer-events-none select-none min-w-[240px] shadow-2xl">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-red-400 to-orange-500 bg-clip-text text-transparent flex items-center gap-2">
            <Crosshair className="w-6 h-6 text-red-500" />
            Wada: Battle Royale
          </h1>
          <p className="text-xs text-gray-400 mt-1">Adaptive Stress Test</p>
          <div className="mt-4 space-y-2 text-sm font-mono border-t border-gray-700 pt-2">
            <div className="flex justify-between items-center">
              <span>Mode:</span> 
              <span className={`font-bold ${hunting ? 'text-red-400 animate-pulse' : 'text-blue-400'}`}>
                {hunting ? 'HUNTER' : 'PASSIVE'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span>Sample N:</span> 
              <span className={`font-bold ${sampleSize < 50 ? 'text-red-500' : 'text-white'}`}>
                {sampleSize} {autoShrink ? '(SHRINKING)' : ''}
              </span>
            </div>
          </div>
        </div>

        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-4 pointer-events-auto z-20">
          <button onClick={() => setIsRunning(!isRunning)} className="p-3 bg-gray-800 hover:bg-gray-700 rounded-full border border-gray-600 shadow-lg">
            {isRunning ? <Pause className="w-6 h-6 text-yellow-400" /> : <Play className="w-6 h-6 text-green-400" />}
          </button>
          
          <button onClick={() => setHunting(!hunting)} className={`p-3 rounded-full border shadow-lg transition-all ${hunting ? 'bg-red-900/50 border-red-500 hover:bg-red-900/80' : 'bg-gray-800 border-gray-600 hover:bg-gray-700'}`} title="Toggle Hunter Mode">
            <Microscope className={`w-6 h-6 ${hunting ? 'text-red-400' : 'text-gray-400'}`} />
          </button>

           <button onClick={() => setView({x:0, y:0, zoom:1})} className="p-3 bg-gray-800 hover:bg-gray-700 rounded-full border border-gray-600 shadow-lg" title="Reset View">
            <Maximize className="w-6 h-6 text-gray-200" />
          </button>

          <button onClick={() => setShowLab(true)} className="p-3 bg-indigo-900/80 hover:bg-indigo-800 rounded-full border border-indigo-500 shadow-lg group relative" title="Open Test Lab">
            <Trophy className="w-6 h-6 text-yellow-400" />
            <span className="absolute -top-12 left-1/2 -translate-x-1/2 px-3 py-1 bg-indigo-950 text-indigo-200 text-xs rounded border border-indigo-700 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
              Battle Royale
            </span>
          </button>
        </div>
      </div>

      {/* RIGHT PANEL - ENTROPY */}
      <div className="w-full md:w-96 bg-gray-950 flex flex-col border-l border-gray-800 shadow-2xl z-10">
        <div className="p-6 border-b border-gray-800 bg-gray-900/50">
          <div className="flex items-center gap-2 mb-2">
            <Map className="w-5 h-5 text-red-500" />
            <h2 className="text-lg font-semibold text-white">Hunter Stream</h2>
          </div>
          <p className="text-sm text-gray-400">
            Entropy from high-stress tracking.
          </p>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-xs">
          {entropyPool.length === 0 && <div className="text-center text-gray-600 mt-10 italic">Hunting Chaos...</div>}
          {entropyPool.slice().reverse().slice(0, 50).map((e, i) => (
            <div key={i} className="flex items-center gap-3 p-2 rounded bg-gray-900 border border-gray-800">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: BASIN_COLORS[e.basin] }} />
              <span className="text-gray-500 w-10 text-right">{e.stress.toFixed(1)}σ</span>
              <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-orange-500 to-red-600" style={{ width: `${Math.min((e.val / 255) * 100, 100)}%` }} />
              </div>
              <span className="ml-auto text-red-400 font-bold min-w-[20px]">{e.val.toString(16).toUpperCase().padStart(2, '0')}</span>
            </div>
          ))}
        </div>
        
        <div className="p-6 bg-gray-900 border-t border-gray-800">
          <div className="flex items-center gap-2 mb-4">
            <Shield className="w-5 h-5 text-purple-400" />
            <h3 className="font-medium text-gray-200">Hunter Key</h3>
          </div>
          <div className="relative group">
            <div className="w-full h-24 p-3 bg-black rounded-lg border border-gray-700 font-mono text-green-500 text-sm break-all overflow-hidden relative flex flex-col justify-center">
              <span className="text-gray-600 text-[10px] uppercase mb-1">Live Feed</span>
              <span className="animate-pulse">{generatedKey || "CALCULATING..."}</span>
            </div>
            <button onClick={() => { navigator.clipboard.writeText(generatedKey); }} className="absolute top-2 right-2 p-1.5 bg-gray-800 rounded hover:bg-gray-700 text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity">
               <Hash className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* --- BATTLE ROYALE LAB --- */}
      {showLab && (
        <div className="absolute inset-0 z-50 bg-black/95 backdrop-blur-xl flex items-center justify-center p-4">
          <button onClick={() => setShowLab(false)} className="absolute top-6 right-6 p-2 bg-gray-800 rounded-full hover:bg-gray-700 text-white z-50">
            <X className="w-6 h-6" />
          </button>
          
          <div className="max-w-7xl w-full flex flex-col gap-6 max-h-[90vh] overflow-y-auto">
            <div className="text-center mb-2">
               <h2 className="text-3xl font-bold bg-gradient-to-r from-indigo-400 to-fuchsia-400 bg-clip-text text-transparent flex items-center justify-center gap-3">
                 <Trophy className="w-8 h-8 text-yellow-400" />
                 Battle Royale: Small Set Stress Test
               </h2>
               <p className="text-gray-400 mt-2">Which algorithm survives low-N sampling?</p>
            </div>
            
            <div className="flex justify-center gap-4 mb-4">
                 <div className="bg-gray-900 px-6 py-3 rounded-xl border border-gray-700 flex items-center gap-4">
                    <span className="text-gray-400 text-sm">Sample Size (N):</span>
                    <input 
                      type="range" min="10" max="500" step="10" 
                      value={sampleSize} 
                      onChange={(e) => setSampleSize(parseInt(e.target.value))}
                      className="w-40 accent-indigo-500"
                    />
                    <span className="text-white font-mono w-10">{sampleSize}</span>
                 </div>
                 
                 <button 
                    onClick={() => setAutoShrink(!autoShrink)}
                    className={`flex items-center gap-2 px-6 py-3 rounded-full border transition-all shadow-xl ${autoShrink ? 'bg-red-900/40 border-red-500 text-red-400 animate-pulse' : 'bg-gray-800 border-gray-600 text-gray-400 hover:bg-gray-700'}`}
                 >
                    <AlertTriangle className="w-5 h-5" />
                    {autoShrink ? 'WEEDING WEAKNESS...' : 'Start Shrink Test'}
                 </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <TestPanel title="Control (PRNG)" color="text-cyan-400" data={controlData} sampleSize={sampleSize} mode="control" />
                <TestPanel title="Wada (Chaos)" color="text-red-400" data={entropyPool.map(e => e.val)} sampleSize={sampleSize} mode="experiment" />
                <TestPanel title="Hybrid (XOR)" color="text-emerald-400" data={hybridData} sampleSize={sampleSize} mode="hybrid" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Updated Test Panel with Score Calculation
function TestPanel({ title, data, color, sampleSize, mode }) {
  const canvasRef = useRef(null);
  
  // 1. Slice data to exact sample size for fairness
  const testSet = data.slice(-sampleSize);
  
  // 2. Calculate Stats
  const { entropy, chiSq } = calculateStats(testSet);
  
  // 3. Score (Heuristic)
  // Perfect Entropy = 8. Perfect ChiSq = 255.
  // Higher ChiSq means LESS uniform (bad).
  // Ideally ChiSq should be close to Degrees of Freedom (255).
  // ChiSq > 300 starts indicating bias.
  
  // Normalize Entropy Score (0-100)
  const entScore = Math.max(0, (entropy - 7.0) * 100); 
  
  // Normalize ChiSq Score (0-100) - Lower ChiSq is better
  // Expected ChiSq ~ 255. 
  const chiDist = Math.abs(chiSq - 255);
  const chiScore = Math.max(0, 100 - (chiDist / 2));
  
  const totalScore = (entScore * 0.6) + (chiScore * 0.4);
  const isWinner = totalScore > 90;
  const isLoser = totalScore < 50;

  useEffect(() => {
    if (!canvasRef.current || testSet.length === 0) return;
    const ctx = canvasRef.current.getContext('2d');
    const width = canvasRef.current.width;
    const height = canvasRef.current.height;
    
    // Scatter Plot
    ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, width, height);
    ctx.strokeStyle = '#1e293b';
    ctx.beginPath();
    for(let i=0; i<=256; i+=32) { ctx.moveTo(i, 0); ctx.lineTo(i, 256); ctx.moveTo(0, i); ctx.lineTo(256, i); }
    ctx.stroke();

    ctx.fillStyle = color.includes('cyan') ? '#22d3ee' : (color.includes('emerald') ? '#34d399' : '#f87171');
    for (let i = 0; i < testSet.length - 1; i++) {
       const x = testSet[i]; const y = testSet[i+1];
       ctx.fillRect(x, 255 - y, 3, 3); // Bigger dots for small N
    }

  }, [testSet, color]);

  return (
    <div className={`rounded-xl border p-6 flex flex-col gap-4 transition-all duration-300 ${isWinner ? 'bg-gray-900 border-green-500 shadow-green-900/20 shadow-2xl scale-105' : (isLoser ? 'bg-red-950/20 border-red-800 opacity-80' : 'bg-gray-900 border-gray-800')}`}>
       <div className="flex justify-between items-center">
          <h3 className={`text-md font-bold ${color} flex items-center gap-2`}>
            {mode === 'hybrid' && <Cpu className="w-4 h-4" />}
            {title}
          </h3>
          <div className="flex flex-col items-end">
              <span className={`text-xl font-mono font-bold ${totalScore > 80 ? 'text-green-400' : (totalScore < 60 ? 'text-red-500' : 'text-yellow-400')}`}>
                {totalScore.toFixed(1)}
              </span>
              <span className="text-[10px] text-gray-500">QUALITY SCORE</span>
          </div>
       </div>
       
       <div className="relative border border-gray-700 rounded-lg overflow-hidden bg-black aspect-square">
          <canvas ref={canvasRef} width={256} height={256} className="w-full h-full" />
          <div className="absolute top-2 left-2 text-[10px] text-gray-500 font-mono bg-black/50 px-1 rounded">
             {testSet.length} SAMPLES
          </div>
       </div>

       <div className="grid grid-cols-2 gap-2 text-xs font-mono">
          <div className="bg-black/30 p-2 rounded flex flex-col">
             <span className="text-gray-500">Entropy</span>
             <span className={entropy > 7.9 ? 'text-green-400' : 'text-yellow-500'}>{entropy.toFixed(3)}</span>
          </div>
          <div className="bg-black/30 p-2 rounded flex flex-col">
             <span className="text-gray-500">Chi-Sq (Bias)</span>
             <span className={Math.abs(chiSq - 255) < 50 ? 'text-green-400' : 'text-red-500'}>{chiSq.toFixed(0)}</span>
          </div>
       </div>
    </div>
  );
}