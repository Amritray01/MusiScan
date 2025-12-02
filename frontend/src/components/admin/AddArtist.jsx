// frontend/src/components/admin/AddArtist.jsx
import React, { useState } from "react";
import { adminAddArtist } from "../../api";

export default function AddArtist(){
  const [name,setName]=useState("");
  const submit=async()=>{
    try{ await adminAddArtist({ name }); alert("Artist added"); setName("") }
    catch(e){ alert(e.message) }
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Add Artist</h3>
      <input className="input mb-3" placeholder="Artist name" value={name} onChange={e=>setName(e.target.value)}/>
      <button className="btn-primary" onClick={submit}>Add Artist</button>
    </div>
  );
}
