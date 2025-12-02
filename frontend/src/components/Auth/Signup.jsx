// frontend/src/components/Auth/Signup.jsx
import React, { useState } from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../firebase";
import { setAuthToken } from "../../api";

export default function Signup({ switchMode }) {
  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const doSignup = async ()=>{
    try{
      const cred = await createUserWithEmailAndPassword(auth, email, password);
      const token = await cred.user.getIdToken();
      setAuthToken(token);
    }catch(e){ alert(e.message) }
  }

  return (
    <div className="card max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4">Create account</h2>
      <input className="input mb-3" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input type="password" className="input mb-4" placeholder="Password (min 6 chars)" value={password} onChange={e=>setPassword(e.target.value)} />
      <button className="btn-primary w-full mb-2" onClick={doSignup}>Sign up</button>
      <button className="btn-ghost w-full" onClick={switchMode}>Back to login</button>
    </div>
  );
}
