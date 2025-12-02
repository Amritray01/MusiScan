// frontend/src/components/admin/AddSong.jsx
import React, { useState } from "react";
import { adminAddSong } from "../../api";

export default function AddSong({ token }){
  const [form,setForm] = useState({ track_name:"", artists:"", album_name:"", track_genre:"", popularity:50 });

  const submit = async ()=>{
    try{
      await adminAddSong(form);
      alert("Song added");
      setForm({ track_name:"", artists:"", album_name:"", track_genre:"", popularity:50 });
    }catch(e){ alert(e.message) }
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Add New Song</h3>
      <div className="grid grid-cols-2 gap-3">
        <input placeholder="Title" className="input" value={form.track_name} onChange={e=>setForm({...form, track_name:e.target.value})}/>
        <input placeholder="Artists" className="input" value={form.artists} onChange={e=>setForm({...form, artists:e.target.value})}/>
        <input placeholder="Album" className="input" value={form.album_name} onChange={e=>setForm({...form, album_name:e.target.value})}/>
        <input placeholder="Genre" className="input" value={form.track_genre} onChange={e=>setForm({...form, track_genre:e.target.value})}/>
      </div>
      <div className="mt-4 flex items-center justify-between">
        <input type="range" min="0" max="100" value={form.popularity} onChange={e=>setForm({...form, popularity:parseInt(e.target.value)})}/>
        <button className="btn-primary" onClick={submit}>Add Song</button>
      </div>
    </div>
  );
}
