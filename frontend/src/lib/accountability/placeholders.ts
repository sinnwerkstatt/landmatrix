// Users placeholders
export const users = [
  { id: 1, name: "Marie", initials: "MG" },
  { id: 2, name: "Jeremy", initials: "JB" },
  { id: 3, name: "Angela", initials: "AH" },
  { id: 4, name: "Nikka", initials: "NR" },
  { id: 5, name: "Coco", initials: "CL" },
  { id: 6, name: "Oleksandra", initials: "OR" },
  { id: 7, name: "Mohamadou", initials: "MD" },
]

// Deals placeholders
const deal1 = {
  id: 1233,
  country: { id: 8, name: "Philippines" },
  status: "pending",
  variables: [
    {
      id: 1,
      status: "no_score",
      score: null,
      assignee: { id: 1, name: "Marie", initials: "MG" },
    },
    { id: 2, status: "no_score", score: null, assignee: null },
    {
      id: 3,
      status: "no_score",
      score: null,
      assignee: { id: 2, name: "Jeremy", initials: "JB" },
    },
    { id: 4, status: "validated", score: 0, assignee: null },
    { id: 5, status: "pending", score: 2, assignee: null },
    { id: 6, status: "pending", score: 1, assignee: null },
    {
      id: 7,
      status: "validated",
      score: 1,
      assignee: { id: 3, name: "Angela", initials: "AH" },
    },
    {
      id: 8,
      status: "validated",
      score: 1,
      assignee: { id: 4, name: "Nikka", initials: "NR" },
    },
    {
      id: 9,
      status: "validated",
      score: 2,
      assignee: { id: 5, name: "Coco", initials: "CL" },
    },
    {
      id: 10,
      status: "validated",
      score: 0,
      assignee: { id: 6, name: "Oleksandra", initials: "OR" },
    },
  ],
}

const deal2 = {
  id: 1234,
  country: { id: 10, name: "Senegal" },
  status: "validated",
  variables: [
    {
      id: 1,
      status: "validated",
      score: null,
      assignee: null,
    },
    { id: 2, status: "validated", score: null, assignee: null },
    {
      id: 3,
      status: "validated",
      score: null,
      assignee: { id: 2, name: "Jeremy", initials: "JB" },
    },
    { id: 4, status: "validated", score: 0, assignee: null },
    { id: 5, status: "validated", score: 2, assignee: null },
    { id: 6, status: "validated", score: 1, assignee: null },
    {
      id: 7,
      status: "validated",
      score: 1,
      assignee: { id: 3, name: "Angela", initials: "AH" },
    },
    { id: 8, status: "validated", score: 1, assignee: null },
    { id: 9, status: "validated", score: 1, assignee: null },
    { id: 10, status: "validated", score: 1, assignee: null },
  ],
}

function makeDeal(id) {
  return {
    id,
    country: { id: 10, name: "Senegal" },
    status: "no_score",
    variables: [
      {
        id: 1,
        status: "no_score",
        score: null,
        assignee: null,
      },
      { id: 2, status: "no_score", score: null, assignee: null },
      { id: 3, status: "no_score", score: null, assignee: null },
      { id: 4, status: "no_score", score: null, assignee: null },
      { id: 5, status: "no_score", score: null, assignee: null },
      { id: 6, status: "no_score", score: null, assignee: null },
      { id: 7, status: "no_score", score: null, assignee: null },
      { id: 8, status: "no_score", score: null, assignee: null },
      { id: 9, status: "validated", score: 2, assignee: null },
      { id: 10, status: "no_score", score: null, assignee: null },
    ],
  }
}

function generateDeals(n) {
  let array = [deal1, deal2]
  let deal_id = 1235
  for (let i = 0; i < n; i++) {
    const newDeal = makeDeal(deal_id)
    array.push(newDeal)
    deal_id = deal_id + 1
  }
  return array
}

export const deals = generateDeals(100)
