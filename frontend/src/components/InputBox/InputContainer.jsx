import { useState } from "react";
import { Search, Sparkles } from "lucide-react";
import getResults from "../../utils/getResults";

const InputContainer = ({ mood, setMood, setRecommendations }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleMoodSubmit = async (e) => {
    e.preventDefault();
    if (!mood.trim()) return;
    setIsAnalyzing(true);

    const results = await getResults(mood);
    const recommendations = {
      emotion: results.analysis.emotion,
      songs: results.recommendations,
    };

    setRecommendations(recommendations);
    setIsAnalyzing(false);
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
