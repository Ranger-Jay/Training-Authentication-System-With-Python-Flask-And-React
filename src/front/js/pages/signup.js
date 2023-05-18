import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import "../../styles/index.css";

export const Signup = () => {
  const { store, actions } = useContext(Context);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  //create State for email and password

  return (
    <div>
      <div className="signup-form">
        <div className="forms">
          <label>Email Address</label>
          <input
            type="email"
            value={email}
            placeholder="Enter your email"
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="forms">
          <label>Password</label>
          <input
            type="password"
            value={password}
            placeholder="Enter your password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>

      <div>
        <button
          onClick={() => actions.sign_up(email, password)}
          className="btn btn-primary"
        >
          Submit
        </button>
      </div>
    </div>

    //create button to send data to endpoint (user information)
  );
};
