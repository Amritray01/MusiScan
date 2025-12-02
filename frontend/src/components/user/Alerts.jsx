// frontend/src/components/user/Alerts.jsx
import React, { useEffect, useState } from "react";
import { getAlerts } from "../../api";

export default function Alerts(){
  const [alerts, setAlerts] = useState([]);

  useEffect(()=>{ getAlerts().then(setAlerts).catch(()=>setAlerts([])) },[]);

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">System Alerts</h3>
      <div className="space-y-3">
        {alerts.length===0 ? <div className="text-[var(--muted)]">No alerts yet.</div> :
          alerts.map((a,i)=>(
            <div key={i} className="p-3 rounded-lg bg-[#071428]">
              <div className="font-medium">{a.alert_type}</div>
              <div className="text-sm text-[var(--muted)]">{a.message}</div>
            </div>
          ))
        }
      </div>
    </div>
  );
}
