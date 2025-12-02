// frontend/src/components/admin/AddAlbum.jsx
import React, { useState } from "react";
import { adminAddAlbum } from "../../api";

export default function AddAlbum(){
  const [form,setForm]=useState({ album_name:"", artists:"", release_date:"" });

  const submit=async()=>{
    try{ await adminAddAlbum(form); alert("Album added"); setForm({album_name:"", artists:"", release_date:""}) }
    catch(e){ alert(e.message) }
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Add Album</h3>
      <input className="input mb-2" placeholder="Album title" value={form.album_name} onChange={e=>setForm({...form,album_name:e.target.value})}/>
      <input className="input mb-2" placeholder="Artists" value={form.artists} onChange={e=>setForm({...form,artists:e.target.value})}/>
      <input type="date" className="input mb-2" value={form.release_date} onChange={e=>setForm({...form,release_date:e.target.value})}/>
      <button className="btn-primary" onClick={submit}>Add Album</button>
    </div>
  );
}
