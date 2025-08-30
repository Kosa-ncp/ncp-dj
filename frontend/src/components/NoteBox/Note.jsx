import { Music } from "lucide-react";

const Note = ({ index }) => {
  return (
    <div
      className="absolute animate-float opacity-10"
      style={{
        left: `${20 + index * 15}%`,
        top: `${30 + (index % 3) * 20}%`,
        animationDelay: `${index * 2}s`,
        animationDuration: "6s",
      }}>
      <Music size={24} className="text-white" />
    </div>
  );
};

export default Note;
