import FeatureItem from "./FeatureItem";

const FeatureContainer = () => {
  const features = [
    {
      icon: "heart",
      title: "감정 인식",
      desc: "AI가 당신의 감정을 정확히 분석해요",
    },
    {
      icon: "music",
      title: "맞춤 추천",
      desc: "감정에 딱 맞는 음악을 골라드려요",
    },
    {
      icon: "play",
      title: "바로 재생",
      desc: "Spotify 연동으로 즉시 들어보세요",
    },
  ];

  return (
    <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
      {features.map((item, index) => (
        <FeatureItem
          key={index}
          icon={item.icon}
          title={item.title}
          desc={item.desc}
        />
      ))}
    </div>
  );
};
export default FeatureContainer;
