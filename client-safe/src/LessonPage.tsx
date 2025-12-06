export default function LessonPage({ videoSrc }: { videoSrc: string }) {
  return (
    <div className="page">
      <div className="videoContainer">
        <video
          src={videoSrc}
          controls
          className="vid"
        />
      </div>

      <div className="rightContent">
        <div className="tts">
          <p>Lorem ipsum dolor sit amet...</p>
        </div>

        <div className="lessonContainer">
          Lesson container
        </div>
      </div>
    </div>
  );
}
