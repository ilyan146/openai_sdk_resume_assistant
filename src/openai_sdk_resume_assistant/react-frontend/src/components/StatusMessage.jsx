import React from 'react';

const StatusMessage = ({ loading, error }) => {
  if (error) return <div className="error">{error}</div>;
  return null;
};

export default StatusMessage;