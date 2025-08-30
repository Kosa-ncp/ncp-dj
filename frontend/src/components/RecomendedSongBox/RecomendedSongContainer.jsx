import { Music, Play, Volume2 } from "lucide-react";

const RecomendedSongContainer = ({ recommendations }) => {
  return (
    <div className="space-y-4 mb-8">
      <h3 className="text-xl font-semibold text-white flex items-center gap-2 mb-6">
        <Volume2 size={24} className="text-purple-400" />
        맞춤 음악 추천
      </h3>

      <div className="grid gap-4">
        {recommendations.songs.map((song, idx) => (
          <div
            key={idx}
            className="bg-white/20 backdrop-blur-sm rounded-xl p-4 flex items-center justify-between hover:bg-white/30 transition-all duration-300 group">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Music size={20} className="text-white" />
              </div>
              <div>
                <h4 className="text-white font-medium">{song.title}</h4>
                <p className="text-blue-200 text-sm">{song.artist}</p>
                <span className="inline-block bg-purple-500/30 text-purple-200 text-xs px-2 py-1 rounded-full mt-1">
                  {song.genre}
                </span>
              </div>
            </div>
            <button className="bg-green-500 hover:bg-green-600 text-white p-3 rounded-full transition-all duration-300 transform group-hover:scale-110">
              <Play size={16} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecomendedSongContainer;
