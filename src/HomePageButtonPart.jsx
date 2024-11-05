import React from "react";
import "./HomePageButtonPart.css";
import { useNavigate } from "react-router-dom";

const HomePageButtonPart = ({ activeButton, setActiveButton }) => {
  const navigate = useNavigate();

  const data = {
    userprofile:
      "https://i.pinimg.com/originals/07/33/ba/0733ba760b29378474dea0fdbcb97107.png",
    buttons: [
      {
        icon: "chatbot.png",
        name: "Chat",
        url: "/",
      },
      {
        icon: "call.png",
        name: "Voice Call",
        url: "/",
      },
    ],
  };

  return (
    <div className="leftpartcontainer">
      <div className="imagepart">
        <img src={data?.userprofile} alt="User Profile" />
      </div>
      <div>
        {data?.buttons.map((ele, index) => (
          <div
            onClick={() => {
              setActiveButton(ele.name);
              navigate(ele?.url);
            }}
            key={index}
            className={`buttonscontainer ${
              activeButton === ele.name ? "active" : ""
            }`}
          >
            <div className="icon">
              <img src={ele?.icon} alt={`${ele.name} icon`} />
            </div>
            <div className="buttonname">{ele?.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePageButtonPart;
