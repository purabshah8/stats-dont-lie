import React from 'react';

export default function Loading() {
  return (
    <div className="lds-container">
      <div className="lds-ring is-centered">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  );
}
