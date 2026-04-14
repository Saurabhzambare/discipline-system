import { useCallback, useState } from 'react';
import PathDiscoveryLayout from './PathDiscoveryLayout';
import QuizOption from './QuizOption';

export default function QuizScreen({ question, onAnswer, submitting }) {
  const [selected, setSelected] = useState(null);

  const handleSelect = useCallback(
    (key) => {
      if (selected || submitting) return;
      setSelected(key);
      setTimeout(() => {
        onAnswer(question.number, key);
        setSelected(null);
      }, 600);
    },
    [onAnswer, question.number, selected, submitting],
  );

  return (
    <PathDiscoveryLayout className="flex items-center justify-center">
      <div className="w-full max-w-xl">
        <h2 className="text-center text-[34px] leading-tight font-semibold mb-10">{question.text}</h2>
        <div className="space-y-3">
          {question.options.map((option, index) => (
            <QuizOption
              key={option.key}
              option={option}
              index={index}
              selected={selected === option.key}
              disabled={Boolean(selected) || submitting}
              onClick={() => handleSelect(option.key)}
            />
          ))}
        </div>
      </div>
    </PathDiscoveryLayout>
  );
}
