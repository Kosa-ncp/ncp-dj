import Note from "./Note";

const NoteContainer = () => {
  return (
    <div className="absolute inset-0 pointer-events-none">
      {[...Array(6)].map((_, i) => (
        <Note key={i} index={i} />
      ))}
    </div>
  );
};

export default NoteContainer;
