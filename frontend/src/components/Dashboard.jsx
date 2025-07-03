import React from 'react';

export default function Dashboard({ tagValues }) {
  return (
    <div className="card">
      <h2 style={{marginBottom:'1em'}}>Live Tag Values</h2>
      {(!tagValues || tagValues.length === 0) ? (
        <div className="center text-muted" style={{flexDirection:'column',minHeight:'80px'}}>
          <svg width="36" height="36" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#e0e7ef"/><path d="M8 16v-1a4 4 0 018 0v1" stroke="#2563eb" strokeWidth="1.5" strokeLinecap="round"/><circle cx="12" cy="10" r="3" fill="#2563eb"/></svg>
          <div style={{marginTop:'0.7em'}}>No tag values to display yet.</div>
        </div>
      ) : (
        <ul style={{margin:0,padding:0,listStyle:'none'}}>
          {tagValues.map((tag, i) => (
            <li key={i} style={{display:'flex',justifyContent:'space-between',padding:'0.7em 0',borderBottom:'1px solid #e5e7eb'}}>
              <span style={{fontWeight:600}}>{tag.name}</span>
              <span>{tag.value}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
} 