import React, { useState } from "react";
import "./HomePage.css";
import HomePageButtonPart from "./HomePageButtonPart";
import HomePageRightPart from "./HomePageRightPart";

const HomePage = () => {
  const [activeButton, setActiveButton] = useState("Chat");

  return (
    <div className="homepagecontainer">
      <div className="rightpart">
        <HomePageButtonPart
          activeButton={activeButton}
          setActiveButton={setActiveButton}
        />
      </div>
      <div className="leftpart">
        <HomePageRightPart activeButton={activeButton} />
      </div>
    </div>
  );
};

export default HomePage;
