import { Heart, Play, Search } from "lucide-react";
import RecomendedSongContainer from "../RecomendedSongBox/RecomendedSongContainer";

const ResultContainer = ({ recommendations, setMood, setRecommendations }) => {
  const resetApp = () => {
    setMood("");
    setRecommendations(null);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
        <div className="text-center mb-8">
          <div className="bg-gradient-to-r from-pink-500 to-purple-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <Heart size={28} className="text-white" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">감정 분석 완료</h2>
          <p className="text-blue-200">
            당신의 현재 감정:{" "}
            <span className="text-purple-300 font-semibold">
              "{recommendations.emotion}"
            </span>
          </p>
        </div>
        <RecomendedSongContainer recommendations={recommendations} />
        <div className="flex gap-4 justify-center">
          <button
            onClick={resetApp}
            className="bg-white/20 hover:bg-white/30 text-white font-medium py-3 px-6 rounded-xl transition-all duration-300 flex items-center gap-2">
            <Search size={20} />
            다른 기분 입력하기
          </button>
          <button className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-medium py-3 px-6 rounded-xl transition-all duration-300 flex items-center gap-2 transform hover:scale-105">
            <Play size={20} />
            Spotify에서 재생
          </button>
        </div>
        <div className="mt-8 text-center">
          <p className="text-blue-200 mb-4">이 추천이 마음에 드시나요?</p>
          <div className="flex justify-center gap-4">
            <button className="bg-white/10 hover:bg-white/20 text-white py-2 px-4 rounded-lg transition-all duration-300">
              👍 좋아요
            </button>
            <button className="bg-white/10 hover:bg-white/20 text-white py-2 px-4 rounded-lg transition-all duration-300">
              👎 다른 곡 추천
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultContainer;
