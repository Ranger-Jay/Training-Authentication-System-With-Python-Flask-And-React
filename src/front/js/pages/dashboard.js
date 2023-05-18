import React, { useContext } from "react";
import { Navigate } from "react-router-dom";

export const Dashboard = () => {
  return localStorage.token ? ( //? means if this exist, show it all, if not, it will be a redirect back to home screen because there is not token
    <div>
      <h1>This is the Dashboard screen only for logged in users.</h1>
    </div>
  ) : (
    <Navigate to="/" />
  );
};
