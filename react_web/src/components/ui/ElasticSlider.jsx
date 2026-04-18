import { animate, motion, useMotionValue, useMotionValueEvent, useTransform } from 'motion/react';
import { useEffect, useRef, useState } from 'react';

const MAX_OVERFLOW = 50;

export default function ElasticSlider({
  defaultValue = 50,
  startingValue = 0,
  maxValue = 100,
  className = '',
  isStepped = false,
  stepSize = 1,
  leftIcon,
  rightIcon,
  readOnly = false
}) {
  return (
    <div className={`slider-container ${className}`} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '1rem', width: '12rem' }}>
      <Slider
        defaultValue={defaultValue}
        startingValue={startingValue}
        maxValue={maxValue}
        isStepped={isStepped}
        stepSize={stepSize}
        leftIcon={leftIcon}
        rightIcon={rightIcon}
        readOnly={readOnly}
      />
    </div>
  );
}

function Slider({ defaultValue, startingValue, maxValue, isStepped, stepSize, leftIcon, rightIcon, readOnly }) {
  const [value, setValue] = useState(defaultValue);
  const sliderRef = useRef(null);
  const [region, setRegion] = useState('middle');
  const clientX = useMotionValue(0);
  const overflow = useMotionValue(0);
  const scale = useMotionValue(1);

  useEffect(() => {
    setValue(defaultValue);
  }, [defaultValue]);

  useMotionValueEvent(clientX, 'change', latest => {
    if (sliderRef.current) {
      const { left, right } = sliderRef.current.getBoundingClientRect();
      let newValue;
      if (latest < left) {
        setRegion('left');
        newValue = left - latest;
      } else if (latest > right) {
        setRegion('right');
        newValue = latest - right;
      } else {
        setRegion('middle');
        newValue = 0;
      }
      overflow.jump(decay(newValue, MAX_OVERFLOW));
    }
  });

  const handlePointerMove = e => {
    if (readOnly) return;
    if (e.buttons > 0 && sliderRef.current) {
      const { left, width } = sliderRef.current.getBoundingClientRect();
      let newValue = startingValue + ((e.clientX - left) / width) * (maxValue - startingValue);
      if (isStepped) {
        newValue = Math.round(newValue / stepSize) * stepSize;
      }
      newValue = Math.min(Math.max(newValue, startingValue), maxValue);
      setValue(newValue);
      clientX.jump(e.clientX);
    }
  };

  const handlePointerDown = e => {
    if (readOnly) return;
    handlePointerMove(e);
    e.currentTarget.setPointerCapture(e.pointerId);
  };

  const handlePointerUp = () => {
    animate(overflow, 0, { type: 'spring', bounce: 0.5 });
  };

  const getRangePercentage = () => {
    const totalRange = maxValue - startingValue;
    if (totalRange === 0) return 0;
    return ((value - startingValue) / totalRange) * 100;
  };

  return (
    <>
      <motion.div
        onHoverStart={() => animate(scale, 1.2)}
        onHoverEnd={() => animate(scale, 1)}
        onTouchStart={() => animate(scale, 1.2)}
        onTouchEnd={() => animate(scale, 1)}
        style={{
          scale,
          opacity: useTransform(scale, [1, 1.2], [0.7, 1]),
          display: 'flex',
          width: '100%',
          touchAction: 'none',
          userSelect: 'none',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '1rem'
        }}
      >
        {leftIcon && (
          <motion.div
            animate={{
              scale: region === 'left' ? [1, 1.4, 1] : 1,
              transition: { duration: 0.25 }
            }}
            style={{
              x: useTransform(() => (region === 'left' ? -overflow.get() / scale.get() : 0)),
              width: 24,
              height: 24,
              color: '#91f1ea'
            }}
          >
            {leftIcon}
          </motion.div>
        )}

        <div
          ref={sliderRef}
          onPointerMove={handlePointerMove}
          onPointerDown={handlePointerDown}
          onPointerUp={handlePointerUp}
          onPointerCancel={handlePointerUp}
          onLostPointerCapture={handlePointerUp}
          style={{
            position: 'relative',
            display: 'flex',
            width: '100%',
            maxWidth: 200,
            flexGrow: 1,
            cursor: readOnly ? 'default' : 'grab',
            touchAction: 'none',
            userSelect: 'none',
            alignItems: 'center',
            padding: '1rem 0',
            pointerEvents: readOnly ? 'none' : 'auto'
          }}
          onMouseDown={(e) => e.currentTarget.style.cursor = 'grabbing'}
          onMouseUp={(e) => e.currentTarget.style.cursor = 'grab'}
        >
          <motion.div
            style={{
              scaleX: useTransform(() => {
                if (sliderRef.current) {
                  const { width } = sliderRef.current.getBoundingClientRect();
                  return 1 + overflow.get() / width;
                }
              }),
              scaleY: useTransform(overflow, [0, MAX_OVERFLOW], [1, 0.8]),
              transformOrigin: useTransform(() => {
                if (sliderRef.current) {
                  const { left, width } = sliderRef.current.getBoundingClientRect();
                  return clientX.get() < left + width / 2 ? 'right' : 'left';
                }
              }),
              height: useTransform(scale, [1, 1.2], [8, 14]),
              marginTop: useTransform(scale, [1, 1.2], [0, -3]),
              marginBottom: useTransform(scale, [1, 1.2], [0, -3]),
              display: 'flex',
              flexGrow: 1
            }}
          >
            <div style={{
              position: 'relative',
              height: '100%',
              flexGrow: 1,
              overflow: 'hidden',
              borderRadius: 9999,
              backgroundColor: 'rgba(39, 241, 57, 0.2)',
              border: '1px solid rgba(39, 241, 57, 0.3)'
            }}>
              <div style={{
                position: 'absolute',
                height: '100%',
                background: 'linear-gradient(90deg, #27f139 0%, #91f1ea 100%)',
                borderRadius: 9999,
                width: `${getRangePercentage()}%`,
                boxShadow: '0 0 15px rgba(39, 241, 57, 0.5), 0 0 30px rgba(145, 241, 234, 0.3)'
              }} />
            </div>
          </motion.div>
        </div>

        {rightIcon && (
          <motion.div
            animate={{
              scale: region === 'right' ? [1, 1.4, 1] : 1,
              transition: { duration: 0.25 }
            }}
            style={{
              x: useTransform(() => (region === 'right' ? overflow.get() / scale.get() : 0)),
              width: 24,
              height: 24,
              color: '#91f1ea'
            }}
          >
            {rightIcon}
          </motion.div>
        )}
      </motion.div>
      <p style={{
        color: '#91f1ea',
        position: 'absolute',
        transform: 'translateY(-1rem)',
        fontSize: '0.875rem',
        fontWeight: 700,
        letterSpacing: '0.05em',
        textShadow: '0 2px 8px rgba(0,0,0,0.5), 0 0 20px rgba(145,241,234,0.3)'
      }}>
        {Math.round(value)}%
      </p>
    </>
  );
}

function decay(value, max) {
  if (max === 0) return 0;
  const entry = value / max;
  const sigmoid = 2 * (1 / (1 + Math.exp(-entry)) - 0.5);
  return sigmoid * max;
}
