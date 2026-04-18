export function CameraIcon({ className = "w-6 h-6" }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 1024 1024" 
      className={className}
    >
      {/* Dark rounded background */}
      <rect 
        x="50" 
        y="50" 
        width="924" 
        height="924" 
        rx="180" 
        fill="#2D3748"
      />
      
      {/* Camera body - white outline */}
      <path 
        d="M 350 280 L 420 220 L 604 220 L 674 280 L 780 280 C 810 280 835 305 835 335 L 835 685 C 835 715 810 740 780 740 L 244 740 C 214 740 189 715 189 685 L 189 335 C 189 305 214 280 244 280 Z" 
        fill="none" 
        stroke="#FFFFFF" 
        strokeWidth="45"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      
      {/* Camera lens outer circle */}
      <circle 
        cx="512" 
        cy="510" 
        r="150" 
        fill="none" 
        stroke="#FFFFFF" 
        strokeWidth="45"
      />
      
      {/* Camera lens inner circle */}
      <circle 
        cx="512" 
        cy="510" 
        r="90" 
        fill="none" 
        stroke="#FFFFFF" 
        strokeWidth="35"
      />
      
      {/* Flash/indicator dot */}
      <circle 
        cx="300" 
        cy="360" 
        r="25" 
        fill="#FFFFFF"
      />
    </svg>
  )
}
