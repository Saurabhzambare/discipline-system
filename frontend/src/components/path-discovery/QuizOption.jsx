export default function QuizOption({ option, selected, disabled, onClick, index }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`w-full rounded-xl border px-4 py-4 text-left text-base transition-all duration-300 min-h-11 ${
        selected
          ? 'border-white bg-[#191924] text-[#E8E8ED] shadow-[0_0_20px_rgba(255,255,255,0.18)]'
          : 'border-[#2A2A3A] bg-[#14141F] text-[#C8C8D1] hover:text-[#E8E8ED]'
      } disabled:cursor-not-allowed`}
      style={{ transitionDelay: `${index * 100}ms` }}
    >
      {option.text}
    </button>
  );
}
