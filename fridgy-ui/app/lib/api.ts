import { ApiResponse } from "@/app/types/interfaces";

export const fetchQueryResponse = async (
  question: string,
): Promise<ApiResponse> => {
  const response = await fetch("http://localhost:5000/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return await response.json();
};
