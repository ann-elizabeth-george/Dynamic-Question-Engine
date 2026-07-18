import './Loader.css';

export default function Loader() {
  return (
    <div className="loader-overlay">
      <div className="loader-spinner">
        <div className="loader-ring"></div>
        <div className="loader-ring"></div>
        <div className="loader-ring"></div>
        <span className="loader-text">Loading...</span>
      </div>
    </div>
  );
}
