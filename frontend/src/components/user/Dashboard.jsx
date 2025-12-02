// frontend/src/components/user/Dashboard.jsx
import React, { useEffect, useState } from "react";
import { fetchSongs } from "../../api";

export default function Dashboard(){
  const [songs,setSongs]=useState([]);

  useEffect(()=>{ fetchSongs().then(setSongs).catch(()=>setSongs([])) },[]);

  // simple aggregation for demo:
  const genreCounts = songs.reduce((acc,s)=>{
    acc[s.track_genre] = (acc[s.track_genre]||0)+1;
    return acc;
  },{})

  return (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Genre Distribution</h3>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(genreCounts).slice(0,6).map(([g,c])=>(
            <div key={g}>
              <div className="flex justify-between text-sm mb-1">
                <span>{g}</span><span className="text-[var(--muted)]">{c}</span>
              </div>
              <div className="h-2 bg-[#06233a] rounded-full"><div className="h-full" style={{width:`${Math.min(100,c*10)}%`, background:`linear-gradient(90deg, var(--accent), var(--indie-pink))`}}/></div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Recent Tracks</h3>
        <div className="space-y-2">
          {songs.slice(0,6).map(s=>(
            <div key={s.track_id} className="flex items-center justify-between p-3 rounded-lg bg-[#071428]">
              <div>
                <div className="font-medium">{s.track_name}</div>
                <div className="text-sm text-[var(--muted)]">{s.artists}</div>
              </div>
              <div className="text-sm text-[var(--muted)]">{s.release_date}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
