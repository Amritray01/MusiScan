// frontend/src/components/Auth/Login.jsx
import React, { useState, useContext } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../firebase";
import { AuthContext } from "../../context/AuthContext";
import { setAuthToken } from "../../api";

export default function Login({ switchMode }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { firebaseUser } = useContext(AuthContext);

  const doLogin = async () => {
    try {
      const cred = await signInWithEmailAndPassword(auth, email, password);
      const token = await cred.user.getIdToken();
      setAuthToken(token);
    } catch (e) {
      alert(e.message);
    }
  };

  return (
    <div className="card max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4">Welcome back</h2>
      <input className="input mb-3" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input type="password" className="input mb-4" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button className="btn-primary w-full mb-2" onClick={doLogin}>Sign in</button>
      <button className="btn-ghost w-full" onClick={switchMode}>Create account</button>
    </div>
  );
}
