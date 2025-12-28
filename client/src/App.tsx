import { useState } from 'react';
import {
  captureScreenshot,
  captureVideo,
  createBatch,
  getBatchStatus,
  getDownloadUrl,
} from './api';
import type { ScreenshotResponse, VideoResponse, BatchStatus } from './api';

type Tab = 'screenshot' | 'video' | 'batch';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('screenshot');

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">Snapsht Service</h1>
          <p className="text-gray-400 text-sm">Screenshot & Video Capture</p>
        </div>
      </header>

      <nav className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex gap-1">
            {(['screenshot', 'video', 'batch'] as Tab[]).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-3 text-sm font-medium capitalize transition-colors ${
                  activeTab === tab
                    ? 'text-blue-400 border-b-2 border-blue-400'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {activeTab === 'screenshot' && <ScreenshotPanel />}
        {activeTab === 'video' && <VideoPanel />}
        {activeTab === 'batch' && <BatchPanel />}
      </main>
    </div>
  );
}

function ScreenshotPanel() {
  const [url, setUrl] = useState('https://example.com');
  const [width, setWidth] = useState(1280);
  const [height, setHeight] = useState(720);
  const [fullPage, setFullPage] = useState(true);
  const [format, setFormat] = useState<'png' | 'jpeg' | 'webp'>('png');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScreenshotResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCapture = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await captureScreenshot({
        url,
        width,
        height,
        full_page: fullPage,
        format,
      });
      setResult(response);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Screenshot failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Capture Screenshot</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">URL</label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
              placeholder="https://example.com"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Width</label>
              <input
                type="number"
                value={width}
                onChange={(e) => setWidth(Number(e.target.value))}
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Height</label>
              <input
                type="number"
                value={height}
                onChange={(e) => setHeight(Number(e.target.value))}
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Format</label>
            <select
              value={format}
              onChange={(e) => setFormat(e.target.value as 'png' | 'jpeg' | 'webp')}
              className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
            >
              <option value="png">PNG</option>
              <option value="jpeg">JPEG</option>
              <option value="webp">WebP</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="fullPage"
              checked={fullPage}
              onChange={(e) => setFullPage(e.target.checked)}
              className="rounded bg-gray-700 border-gray-600"
            />
            <label htmlFor="fullPage" className="text-sm text-gray-300">Full page screenshot</label>
          </div>

          <button
            onClick={handleCapture}
            disabled={loading || !url}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-medium py-2 px-4 rounded transition-colors"
          >
            {loading ? 'Capturing...' : 'Capture Screenshot'}
          </button>

          {error && (
            <div className="bg-red-900/50 border border-red-700 rounded p-3 text-red-300 text-sm">
              {error}
            </div>
          )}
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Result</h2>

        {result ? (
          <div className="space-y-4">
            <div className="aspect-video bg-gray-700 rounded overflow-hidden">
              <img
                src={getDownloadUrl(result.download_url)}
                alt="Screenshot"
                className="w-full h-full object-contain"
              />
            </div>

            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="text-gray-400">Dimensions:</div>
              <div>{result.dimensions.width} x {result.dimensions.height}</div>
              <div className="text-gray-400">Size:</div>
              <div>{(result.size / 1024).toFixed(1)} KB</div>
              <div className="text-gray-400">Format:</div>
              <div>{result.format.toUpperCase()}</div>
            </div>

            <a
              href={getDownloadUrl(result.download_url)}
              download={result.filename}
              className="block w-full bg-green-600 hover:bg-green-700 text-white text-center font-medium py-2 px-4 rounded transition-colors"
            >
              Download
            </a>
          </div>
        ) : (
          <div className="aspect-video bg-gray-700 rounded flex items-center justify-center text-gray-500">
            Screenshot preview will appear here
          </div>
        )}
      </div>
    </div>
  );
}

function VideoPanel() {
  const [url, setUrl] = useState('https://example.com');
  const [duration, setDuration] = useState(5000);
  const [fps, setFps] = useState(24);
  const [format, setFormat] = useState<'mp4' | 'webm' | 'gif'>('mp4');
  const [scrollSpeed, setScrollSpeed] = useState<'slow' | 'medium' | 'fast'>('medium');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VideoResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCapture = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await captureVideo({
        url,
        duration,
        fps,
        format,
        scroll_speed: scrollSpeed,
      });
      setResult(response);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Video capture failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Capture Video</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">URL</label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Duration (ms)</label>
              <input
                type="number"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">FPS</label>
              <input
                type="number"
                value={fps}
                onChange={(e) => setFps(Number(e.target.value))}
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Format</label>
              <select
                value={format}
                onChange={(e) => setFormat(e.target.value as 'mp4' | 'webm' | 'gif')}
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
              >
                <option value="mp4">MP4</option>
                <option value="webm">WebM</option>
                <option value="gif">GIF</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Scroll Speed</label>
              <select
                value={scrollSpeed}
                onChange={(e) => setScrollSpeed(e.target.value as 'slow' | 'medium' | 'fast')}
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
              >
                <option value="slow">Slow</option>
                <option value="medium">Medium</option>
                <option value="fast">Fast</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleCapture}
            disabled={loading || !url}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-medium py-2 px-4 rounded transition-colors"
          >
            {loading ? 'Capturing...' : 'Capture Video'}
          </button>

          {error && (
            <div className="bg-red-900/50 border border-red-700 rounded p-3 text-red-300 text-sm">
              {error}
            </div>
          )}
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Result</h2>

        {result ? (
          <div className="space-y-4">
            <div className="aspect-video bg-gray-700 rounded overflow-hidden">
              {result.format === 'gif' ? (
                <img
                  src={getDownloadUrl(result.download_url)}
                  alt="Video GIF"
                  className="w-full h-full object-contain"
                />
              ) : (
                <video
                  src={getDownloadUrl(result.download_url)}
                  controls
                  className="w-full h-full"
                />
              )}
            </div>

            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="text-gray-400">Duration:</div>
              <div>{(result.duration / 1000).toFixed(1)}s</div>
              <div className="text-gray-400">Size:</div>
              <div>{(result.size / 1024 / 1024).toFixed(2)} MB</div>
              <div className="text-gray-400">Format:</div>
              <div>{result.format.toUpperCase()}</div>
            </div>

            <a
              href={getDownloadUrl(result.download_url)}
              download={result.filename}
              className="block w-full bg-green-600 hover:bg-green-700 text-white text-center font-medium py-2 px-4 rounded transition-colors"
            >
              Download
            </a>
          </div>
        ) : (
          <div className="aspect-video bg-gray-700 rounded flex items-center justify-center text-gray-500">
            Video preview will appear here
          </div>
        )}
      </div>
    </div>
  );
}

function BatchPanel() {
  const [urls, setUrls] = useState('https://example.com\nhttps://google.com');
  const [fullPage, setFullPage] = useState(true);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<BatchStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    const urlList = urls.split('\n').map(u => u.trim()).filter(u => u);
    if (urlList.length === 0) return;

    setLoading(true);
    setError(null);
    setStatus(null);

    try {
      const response = await createBatch(urlList, { full_page: fullPage });
      pollStatus(response.batch_id);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Batch creation failed');
      setLoading(false);
    }
  };

  const pollStatus = async (id: string) => {
    try {
      const statusData = await getBatchStatus(id);
      setStatus(statusData);

      if (statusData.status === 'processing' || statusData.status === 'pending') {
        setTimeout(() => pollStatus(id), 2000);
      } else {
        setLoading(false);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to get status');
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Batch Screenshots</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">
              URLs (one per line)
            </label>
            <textarea
              value={urls}
              onChange={(e) => setUrls(e.target.value)}
              rows={6}
              className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white font-mono text-sm"
              placeholder="https://example.com&#10;https://google.com"
            />
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="batchFullPage"
              checked={fullPage}
              onChange={(e) => setFullPage(e.target.checked)}
              className="rounded bg-gray-700 border-gray-600"
            />
            <label htmlFor="batchFullPage" className="text-sm text-gray-300">Full page screenshots</label>
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading || !urls.trim()}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-medium py-2 px-4 rounded transition-colors"
          >
            {loading ? 'Processing...' : 'Start Batch'}
          </button>

          {error && (
            <div className="bg-red-900/50 border border-red-700 rounded p-3 text-red-300 text-sm">
              {error}
            </div>
          )}
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Progress</h2>

        {status ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-400">Status:</span>
              <span className={`font-medium ${
                status.status === 'completed' ? 'text-green-400' :
                status.status === 'failed' ? 'text-red-400' : 'text-yellow-400'
              }`}>
                {status.status.toUpperCase()}
              </span>
            </div>

            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${status.progress}%` }}
              />
            </div>

            <div className="grid grid-cols-4 gap-2 text-center text-sm">
              <div>
                <div className="text-2xl font-bold text-green-400">{status.completed}</div>
                <div className="text-gray-500">Done</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-yellow-400">{status.processing}</div>
                <div className="text-gray-500">Running</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-400">{status.pending}</div>
                <div className="text-gray-500">Pending</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-red-400">{status.failed}</div>
                <div className="text-gray-500">Failed</div>
              </div>
            </div>

            <div className="max-h-64 overflow-y-auto space-y-2">
              {status.jobs.map((job) => (
                <div
                  key={job.id}
                  className="flex items-center justify-between bg-gray-700 rounded p-2 text-sm"
                >
                  <span className="truncate flex-1 mr-2">{job.url}</span>
                  {job.status === 'completed' && job.result ? (
                    <a
                      href={getDownloadUrl(job.result.download_url)}
                      download
                      className="text-blue-400 hover:text-blue-300"
                    >
                      Download
                    </a>
                  ) : job.status === 'failed' ? (
                    <span className="text-red-400">Failed</span>
                  ) : (
                    <span className="text-yellow-400">{job.status}</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="h-64 bg-gray-700 rounded flex items-center justify-center text-gray-500">
            Batch progress will appear here
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
