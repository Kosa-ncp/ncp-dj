import { Headphones } from "lucide-react";

const Header = () => {
  return (
    <header className="text-center mb-12">
      <div className="flex justify-center items-center gap-3 mb-4">
        <div className="bg-gradient-to-r from-pink-500 to-purple-500 p-3 rounded-full">
          <Headphones size={32} className="text-white" />
        </div>
        <h1 className="text-4xl font-bold text-white">MoodTunes</h1>
      </div>
      <p className="text-xl text-blue-100 mb-2">
        당신의 감정에 어울리는 완벽한 음악을 찾아드려요
      </p>
      <p className="text-blue-200 opacity-80">
        지금 기분이나 상황을 자유롭게 표현해보세요
      </p>
    </header>
  );
};

export default Header;
