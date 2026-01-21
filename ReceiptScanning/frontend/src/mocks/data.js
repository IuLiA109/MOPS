export const mockUser = {
  id: 1,
  username: "alex",
  email: "alex@test.com"
};

export const mockScanResult = {
  produse: [
    { name: "Lapte Zuzu", price: 8.99, category: "Lactate" },
    { name: "Paine alba", price: 4.50, category: "Panificatie" },
    { name: "Unt President", price: 12.30, category: "Lactate" },
    { name: "Mere", price: 6.20, category: "Fructe" },
    { name: "Piept pui", price: 23.50, category: "Carne" }
  ],
  total: 55.49
};

export const mockReceipts = [
  {
    id: 1,
    date: "2025-01-20",
    store: "Kaufland",
    total: 55.49,
    produse: [
      { name: "Lapte Zuzu", price: 8.99, category: "Lactate" },
      { name: "Paine alba", price: 4.50, category: "Panificatie" }
    ]
  },
  {
    id: 2,
    date: "2025-01-18",
    store: "Lidl",
    total: 89.20,
    produse: [
      { name: "Unt President", price: 12.30, category: "Lactate" },
      { name: "Mere", price: 6.20, category: "Fructe" }
    ]
  },
  {
    id: 3,
    date: "2025-01-15",
    store: "Carrefour",
    total: 120.00,
    produse: [
      { name: "Piept pui", price: 23.50, category: "Carne" }
    ]
  }
];

export const mockMonthlyStats = {
  totalSpent: 264.69,
  receiptCount: 3,
  byCategory: [
    { category: "Lactate", amount: 21.29 },
    { category: "Panificatie", amount: 4.50 },
    { category: "Fructe", amount: 6.20 },
    { category: "Carne", amount: 23.50 }
  ]
};
