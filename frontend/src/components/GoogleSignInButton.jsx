import { useEffect, useRef } from 'react';

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || '';

function loadGsiScript(callback) {
  if (window.google?.accounts?.id) {
    callback();
    return;
  }
  const existing = document.getElementById('google-gsi-script');
  if (existing) {
    existing.addEventListener('load', callback);
    return;
  }
  const script = document.createElement('script');
  script.id = 'google-gsi-script';
  script.src = 'https://accounts.google.com/gsi/client';
  script.async = true;
  script.defer = true;
  script.addEventListener('load', callback);
  document.head.appendChild(script);
}

export default function GoogleSignInButton({ onCredential, disabled }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!GOOGLE_CLIENT_ID || disabled) return;

    loadGsiScript(() => {
      if (!containerRef.current || !window.google?.accounts?.id) return;
      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: (response) => onCredential(response.credential),
      });
      window.google.accounts.id.renderButton(containerRef.current, {
        theme: 'filled_black',
        size: 'large',
        width: containerRef.current.offsetWidth || 320,
        text: 'continue_with',
        shape: 'rectangular',
      });
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [disabled]);

  if (!GOOGLE_CLIENT_ID) {
    return null;
  }

  return (
    <div
      ref={containerRef}
      className={`w-full overflow-hidden rounded-lg ${disabled ? 'pointer-events-none opacity-50' : ''}`}
    />
  );
}
