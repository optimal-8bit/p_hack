/**
 * Video Helper - Manages background videos for streaming state
 */

// Import videos from the videos folder
// Note: Videos should be placed in src/videos/ folder
const videos = [
  '/videos/video1.mp4',
  '/videos/video2.mp4',
  '/videos/video3.mp4',
];

/**
 * Get a random video from the available videos
 * @returns {string} - Path to a random video
 */
export const getRandomVideo = () => {
  const randomIndex = Math.floor(Math.random() * videos.length);
  return videos[randomIndex];
};

/**
 * Preload a video to ensure smooth playback
 * @param {string} videoSrc - Path to the video
 * @returns {Promise} - Resolves when video is loaded
 */
export const preloadVideo = (videoSrc) => {
  return new Promise((resolve, reject) => {
    const video = document.createElement('video');
    video.src = videoSrc;
    video.preload = 'auto';
    video.onloadeddata = () => resolve(video);
    video.onerror = () => reject(new Error('Failed to load video'));
  });
};

/**
 * Check if videos exist in the videos folder
 * @returns {boolean} - True if videos are available
 */
export const hasVideos = () => {
  return videos.length > 0;
};

export default {
  getRandomVideo,
  preloadVideo,
  hasVideos,
};
