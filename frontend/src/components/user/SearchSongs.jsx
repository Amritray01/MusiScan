// frontend/src/components/user/SearchSongs.jsx
import React, { useContext, useEffect, useState } from "react";
import { Search } from "lucide-react";
import { searchSongs, autocomplete } from "../../api";
import { AuthContext } from "../../context/AuthContext";

export default function SearchSongs(){
  const [q,setQ] = useState("");
  const [results,setResults] = useState([]);
  const [suggestions,setSuggestions] = useState([]);

  useEffect(()=>{ if(q.length>1){
    autocomplete(q).then(s=>{
      // suggestion objects from ES; map to simple text
      setSuggestions(s.map(opt => opt.text || (opt._source && opt._source.track_name)).slice(0,6))
    }).catch(()=>setSuggestions([]))
  }else setSuggestions([]) },[q])

  const doSearch = async ()=>{
    if(!q) return setResults([]);
    const r = await searchSongs(q);
    setResults(r);
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <div className="flex items-center">
          <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search songs, artists, genres..." className="input flex-1 mr-3 text-sm" onKeyDown={e=>e.key==='Enter' && doSearch()}/>
          <button className="btn-primary" onClick={doSearch}><Search/></button>
        </div>
        {suggestions.length>0 && (
          <div className="mt-3 grid grid-cols-3 gap-2">
            {suggestions.map(s=> <button key={s} onClick={()=>{setQ(s); setSuggestions([]);}} className="btn-ghost text-xs">{s}</button>)}
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="font-semibold mb-3">Results ({results.length})</h3>
        <div className="space-y-3">
          {results.map((s,idx)=>(
            <div key={s.track_id || idx} className="flex items-center justify-between p-3 rounded-lg bg-[#071428] border border-[#0e2736]">
              <div>
                <div className="font-medium">{s.track_name}</div>
                <div className="text-sm text-[var(--muted)]">{s.artists} • {s.album_name}</div>
              </div>
              <div className="text-right">
                <div className="text-sm">{s.track_genre}</div>
                <div className="text-xs text-[var(--muted)]">Popularity {s.popularity}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
