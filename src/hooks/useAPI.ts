import { useCallback } from 'react';
import { apiFetch, apiGet, apiPost, apiPut, apiPatch, apiDelete, apiResponse } from '../utils/apiClient';

/**
 * Hook for making API calls with automatic token management
 */
export function useAPI() {
  const fetch = useCallback(apiFetch, []);
  const get = useCallback(apiGet, []);
  const post = useCallback(apiPost, []);
  const put = useCallback(apiPut, []);
  const patch = useCallback(apiPatch, []);
  const del = useCallback(apiDelete, []);
  const handleResponse = useCallback(apiResponse, []);

  return {
    fetch,
    get,
    post,
    put,
    patch,
    delete: del,
    handleResponse,
  };
}
