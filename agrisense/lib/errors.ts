/**
 * API error normalization and handling
 */

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}

export async function handleApiResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMsg = `API error: ${response.status}`;
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMsg = typeof errorData.detail === "string"
          ? errorData.detail
          : JSON.stringify(errorData.detail);
      }
    } catch (parseErr) {
      // Ignore JSON parse errors
    }

    const error: ApiError = {
      message: errorMsg,
      status: response.status,
    };
    throw error;
  }

  return response.json();
}

export function isEmptyDataResponse(data: any): boolean {
  return (
    data?.recent_prices?.length === 0 ||
    (Array.isArray(data?.data) && data.data.length === 0) ||
    (data?.message && !data?.crop_name)
  );
}
