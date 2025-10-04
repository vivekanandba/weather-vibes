import api from './api';
import { AdvisorRequest, AdvisorResponse } from '../types/api';

export const advisorService = {
  getRecommendations: async (request: AdvisorRequest): Promise<AdvisorResponse> => {
    const response = await api.post<AdvisorResponse>('/api/advisor', request);
    return response.data;
  },
};
