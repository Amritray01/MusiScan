// frontend/src/context/AuthContext.jsx
import React, { createContext, useEffect, useState } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [firebaseUser, setFirebaseUser] = useState(null);
  const [token, setToken] = useState(null);
  const [claims, setClaims] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (user) => {
      if (user) {
        setFirebaseUser(user);
        const id = await user.getIdToken();
        setToken(id);
        const idRes = await user.getIdTokenResult();
        setClaims(idRes.claims || {});
      } else {
        setFirebaseUser(null);
        setToken(null);
        setClaims({});
      }
      setLoading(false);
    });
    return () => unsub();
  }, []);

  return (
    <AuthContext.Provider value={{ firebaseUser, token, claims, loading }}>
      {children}
    </AuthContext.Provider>
  );
}
