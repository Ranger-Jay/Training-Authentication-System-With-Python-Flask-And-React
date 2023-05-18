import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { Link } from "react-router-dom";

export const Home = () => {
  const { store, actions } = useContext(Context);

  return (
    <div className="home">
      <div>
        <h1>Welcome to The Star Wars Project</h1>
      </div>
      <div className="buttons">
        <Link to={"/signup"}>
          <button>Sign Up</button>
        </Link>
        <Link to={"/login"}>
          <button>Log In</button>
        </Link>
      </div>
    </div>
  );
};
