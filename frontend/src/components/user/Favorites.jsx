// frontend/src/components/user/Favorites.jsx
import React, { useEffect, useState, useContext } from "react";
import { getFavorites, removeFavorite } from "../../api";
import { AuthContext } from "../../context/AuthContext";
import { Heart } from "lucide-react";

export default function Favorites(){
  const { loading } = useContext(AuthContext);
  const [favs,setFavs] = useState([]);

  useEffect(()=>{
    if(loading) return;
    getFavorites().then(setFavs).catch(()=>setFavs([]));
  },[loading]);

  const doRemove = async (item) => {
    await removeFavorite({ item_type: item.item_type, item_value: item.item_value });
    setFavs(prev => prev.filter(p => !(p.item_type===item.item_type && p.item_value===item.item_value)));
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Your Favorites</h3>
      {favs.length===0 ? <div className="text-[var(--muted)]">No favorites yet — add songs or artists from search.</div> :
        <div className="space-y-3">
          {favs.map(f=>(
            <div key={f.item_value} className="flex items-center justify-between p-3 rounded-lg bg-[#071428]">
              <div>
                <div className="font-medium">{f.item_value}</div>
                <div className="text-sm text-[var(--muted)]">{f.item_type}</div>
              </div>
              <button onClick={()=>doRemove(f)} className="btn-ghost"><Heart className="text-[var(--accent)]"/></button>
            </div>
          ))}
        </div>
      }
    </div>
  );
}
