import React from "react";
import "./HomePageRightPart.css";
import ChatSection from "./ChatSection";
import VoiceCall from "./VoiceCall";

const HomePageRightPart = ({ activeButton }) => {
  return (
    <div className="rightpartcontainer">
      <div>
        {activeButton === "Chat" && (
          <div>
            <div>Chat </div>
            <div>
              <ChatSection />
            </div>
          </div>
        )}
        {activeButton === "Voice Call" && (
          <div>
            <div>Voice Call</div>
            <div>
              <VoiceCall />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePageRightPart;
