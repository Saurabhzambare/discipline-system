function IconBase({ children, color = '#E8E8ED', className = 'h-6 w-6' }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} style={{ color }}>
      {children}
    </svg>
  );
}

export default function PathIcon({ pathCode, color, className }) {
  if (pathCode === 'fitness_warrior') {
    return (
      <IconBase color={color} className={className}>
        <path d="M8 5l8 8M16 5l-8 8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M6 17l2 2M16 17l2 2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      </IconBase>
    );
  }
  if (pathCode === 'mindset_sage') {
    return (
      <IconBase color={color} className={className}>
        <path d="M12 4a3 3 0 013 3c0 1.1-.6 2.1-1.5 2.6v1.4h1.4A2.6 2.6 0 0117.5 13v1A2.5 2.5 0 0115 16.5h-6A2.5 2.5 0 016.5 14v-1A2.6 2.6 0 019.1 11h1.4V9.6A3 3 0 019 7a3 3 0 013-3z" stroke="currentColor" strokeWidth="1.7" />
        <path d="M10 19h4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      </IconBase>
    );
  }
  if (pathCode === 'health_alchemist') {
    return (
      <IconBase color={color} className={className}>
        <path d="M9 4h6M10 4v5l-3.5 6.2A3 3 0 009.1 20h5.8a3 3 0 002.6-4.8L14 9V4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </IconBase>
    );
  }

  if (pathCode === 'locked') {
    return (
      <IconBase color={color} className={className}>
        <rect x="7" y="11" width="10" height="8" rx="2" stroke="currentColor" strokeWidth="1.8" />
        <path d="M9 11V9a3 3 0 016 0v2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      </IconBase>
    );
  }
  if (pathCode === 'discipline_knight') {
    return (
      <IconBase color={color} className={className}>
        <path d="M12 4l6 2v5c0 4.1-2.4 6.9-6 9-3.6-2.1-6-4.9-6-9V6l6-2z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
      </IconBase>
    );
  }
  return (
    <IconBase color={color} className={className}>
      <path d="M12 4c2.2 0 4 1.7 4 3.9 0 1.3-.7 2.5-1.9 3.2.6.7 1.4 1.2 2.3 1.4 1.4.3 2.2 1.7 1.8 3.1-.6 2.4-2.8 4.1-5.2 4.1-3 0-5.4-2.4-5.4-5.4 0-1.9 1-3.6 2.5-4.5A4 4 0 018 7.9C8 5.7 9.8 4 12 4z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
    </IconBase>
  );
}
