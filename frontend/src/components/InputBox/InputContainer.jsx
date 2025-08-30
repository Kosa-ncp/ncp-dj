import { useState } from "react";
import { Search, Sparkles } from "lucide-react";

const InputContainer = ({ mood, setMood, setRecommendations }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const getResults = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/");

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      return null;
    }
  };

  const handleMoodSubmit = async (e) => {
    e.preventDefault();
    if (!mood.trim()) return;

    const results = await getResults(mood);

    console.log(results);

    setIsAnalyzing(true);

    setTimeout(() => {
      const mockRecommendations = {
        emotion:
          mood.includes("슬픔") || mood.includes("우울")
            ? "슬픔"
            : mood.includes("기쁘") || mood.includes("행복")
            ? "기쁨"
            : mood.includes("화나") || mood.includes("짜증")
            ? "분노"
            : mood.includes("외로")
            ? "외로움"
            : "평온",
        songs: [
          { title: "Spring Day", artist: "BTS", genre: "K-Pop" },
          { title: "Through the Night", artist: "IU", genre: "Ballad" },
          { title: "Palette", artist: "IU ft. G-Dragon", genre: "R&B" },
          { title: "Eight", artist: "IU & SUGA", genre: "Pop" },
        ],
      };
      setRecommendations(mockRecommendations);
      setIsAnalyzing(false);
    }, 2000);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
        <div className="space-y-6">
          <div className="space-y-3">
            <label className="text-lg font-medium text-white flex items-center gap-2">
              <Sparkles size={20} className="text-yellow-400" />
              지금 어떤 기분이신가요?
            </label>
            <textarea
              value={mood}
              onChange={(e) => setMood(e.target.value)}
              placeholder="예: 비가 와서 우울해요... / 오늘 승진해서 너무 기뻐요! / 혼자 있어서 외로워요"
              className="w-full h-32 px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
              disabled={isAnalyzing}
            />
          </div>

          <button
            type="submit"
            onClick={handleMoodSubmit}
            disabled={!mood.trim() || isAnalyzing}
            className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 disabled:scale-100 flex items-center justify-center gap-3 shadow-lg">
            {isAnalyzing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                감정 분석 중...
              </>
            ) : (
              <>
                <Search size={20} />
                음악 추천받기
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default InputContainer;
