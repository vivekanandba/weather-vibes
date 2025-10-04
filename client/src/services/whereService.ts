import api from './api';
import { WhereRequest, WhereResponse } from '../types/api';

export const whereService = {
  getHeatmap: async (request: WhereRequest): Promise<WhereResponse> => {
    const response = await api.post<WhereResponse>('/api/where', request);
    return response.data;
  },
};
