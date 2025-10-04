import api from './api';
import { WhenRequest, WhenResponse } from '../types/api';

export const whenService = {
  getMonthlyScores: async (request: WhenRequest): Promise<WhenResponse> => {
    const response = await api.post<WhenResponse>('/api/when', request);
    return response.data;
  },
};
