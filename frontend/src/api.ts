import axios from "axios";

export type ServerConfig = {
  maxFileSize: number;
  allowedTypes: string[];
  mountPath: string;
};

export type UploadSuccessResult = {
  filename: string;
  status: 201;
  id: string;
  url: string;
  size: number;
  content_type: string;
  uploaded_at: number;
};

export type UploadErrorResult = {
  filename: string;
  status: 413 | 415;
  error: string;
  message: string;
};

export type UploadResult = UploadSuccessResult | UploadErrorResult;

const client = axios.create();

export async function fetchConfig(): Promise<ServerConfig> {
  const response = await client.get<ServerConfig>("/api/v1/config");
  return response.data;
}

export async function uploadImages(files: File[]) {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  const response = await client.post<{ uploaded: UploadSuccessResult[] } | { results: UploadResult[] }>(
    "/api/v1/images",
    formData,
  );

  return {
    status: response.status,
    data: response.data,
  };
}
