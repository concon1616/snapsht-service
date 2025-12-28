const API_BASE = 'http://localhost:8000';

export interface ScreenshotRequest {
  url: string;
  width?: number;
  height?: number;
  full_page?: boolean;
  format?: 'png' | 'jpeg' | 'webp';
  quality?: number;
  wait_for?: number;
  selector?: string;
  dismiss_popups?: boolean;
}

export interface ScreenshotResponse {
  id: string;
  filename: string;
  size: number;
  format: string;
  dimensions: { width: number; height: number };
  full_page: boolean;
  download_url: string;
  created_at: string;
}

export interface VideoRequest {
  url: string;
  width?: number;
  height?: number;
  duration?: number;
  fps?: number;
  format?: 'mp4' | 'webm' | 'gif';
  scroll_speed?: 'slow' | 'medium' | 'fast';
}

export interface VideoResponse {
  id: string;
  filename: string;
  size: number;
  format: string;
  dimensions: { width: number; height: number };
  duration: number;
  fps: number;
  download_url: string;
  created_at: string;
}

export interface BatchResponse {
  batch_id: string;
  total_jobs: number;
  status_url: string;
}

export interface BatchStatus {
  batch_id: string;
  total_jobs: number;
  completed: number;
  failed: number;
  processing: number;
  pending: number;
  status: string;
  progress: number;
  jobs: Array<{
    id: string;
    url: string;
    status: string;
    result?: { download_url: string };
    error?: string;
  }>;
}

export async function captureScreenshot(request: ScreenshotRequest): Promise<ScreenshotResponse> {
  const response = await fetch(`${API_BASE}/api/screenshot`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Screenshot failed');
  }

  return response.json();
}

export async function captureVideo(request: VideoRequest): Promise<VideoResponse> {
  const response = await fetch(`${API_BASE}/api/video`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Video capture failed');
  }

  return response.json();
}

export async function createBatch(urls: string[], options?: Partial<ScreenshotRequest>): Promise<BatchResponse> {
  const response = await fetch(`${API_BASE}/api/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ urls, options }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Batch creation failed');
  }

  const data = await response.json();
  return data;
}

export async function getBatchStatus(batchId: string): Promise<BatchStatus> {
  const response = await fetch(`${API_BASE}/api/batch/${batchId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get batch status');
  }

  const data = await response.json();
  return data.batch;
}

export function getDownloadUrl(path: string): string {
  return `${API_BASE}${path}`;
}
