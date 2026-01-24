import apiClient from './client';

export type AccountType = 'cash' | 'bank' | 'card' | 'other';

export interface Account {
  id: number;
  user_id: number;
  name: string;
  type: AccountType;
  currency: string;
  is_default: boolean;
  created_at: string;
}

export interface AccountWithBalance extends Account {
  balance: number;
  transaction_count: number;
}

export const accountApi = {
  getById: async (accountId: number): Promise<Account> => {
    return apiClient.get<Account>(`/accounts/${accountId}`);
  },
  getDetails: async (accountId: number): Promise<AccountWithBalance> => {
    return apiClient.get<AccountWithBalance>(`/accounts/${accountId}/details`);
  },
};

export default accountApi;
