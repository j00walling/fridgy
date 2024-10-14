import React from "react";

interface Query {
  question: string;
  response: string;
  timestamp: Date;
}

const QueryResponse = ({ queries }: { queries: Query[] }) => {
  return (
    <div className="space-y-4">
      {queries.map((query, index) => (
        <div key={index} className="border rounded p-4">
          <p className="font-bold">You: {query.question}</p>
          <p>Fridgy: {query.response}</p>
        </div>
      ))}
    </div>
  );
};

export default QueryResponse;
