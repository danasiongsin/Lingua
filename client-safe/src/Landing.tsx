interface LandingProps {
  onSelectVideo: (src: string) => void;
}

export default function Landing({ onSelectVideo }: LandingProps) {
  const videos = [
    { id: 1, src: "../../english_final.mp4" },
    { id: 2, src: "../../french_final.mp4" },
    { id: 3, src: "../../spanish_final.mp4" },
  ];

  return (
    <div className="landing">
      <h1>Select your video</h1>

      <div className="video-options">
        {videos.map(v => (
          <div key={v.id} className="video-option">
            <video
              src={v.src}
              className="thumbnail"
              onClick={() => onSelectVideo(v.src)}
            />
            <button onClick={() => onSelectVideo(v.src)}>Choose</button>
          </div>
        ))}
      </div>
    </div>
  );
}
