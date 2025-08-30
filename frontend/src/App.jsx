import { useState } from "react";
import "./App.css";
import Container from "./components/Main/Container";
import InputContainer from "./components/InputBox/InputContainer";
import FeatureContainer from "./components/FeatureBox/FeatureContainer";
import ResultContainer from "./components/ResultBox/ResultContainer";

const MoodMusicApp = () => {
  const [mood, setMood] = useState("");
  const [recommendations, setRecommendations] = useState(null);

  return (
    <>
      <Container>
        {!recommendations ? (
          <InputContainer
            mood={mood}
            setMood={setMood}
            setRecommendations={setRecommendations}
          />
        ) : (
          <ResultContainer
            recommendations={recommendations}
            setRecommendations={setRecommendations}
            setMood={setMood}
          />
        )}
        <FeatureContainer />
      </Container>
    </>
  );
};

export default MoodMusicApp;
