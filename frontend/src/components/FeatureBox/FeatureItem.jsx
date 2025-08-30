import { DynamicIcon } from "lucide-react/dynamic";

const FeatureItem = ({ index, icon, title, desc }) => {
  return (
    <div
      key={index}
      className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 text-center border border-white/10 hover:bg-white/10 transition-all duration-300">
      <DynamicIcon
        name={icon}
        size={32}
        className="text-purple-400 mx-auto mb-3"
      />
      <h3 className="text-white font-semibold mb-2">{title}</h3>
      <p className="text-blue-200 text-sm">{desc}</p>
    </div>
  );
};

export default FeatureItem;
