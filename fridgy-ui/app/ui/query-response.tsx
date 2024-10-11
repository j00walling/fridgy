import React from "react";

interface QueryResponseProps {
  queries: { question: string; response: string }[];
}

const QueryResponse: React.FC<QueryResponseProps> = ({ queries }) => {
  return (
    <div className="flex flex-col mb-4 w-[80%]">
      {queries.map((q, index) => (
        <div key={index} className="mb-2">
          <p className="font-bold">You: {q.question}</p>
          <p className="italic">Fridgy: {q.response}</p>
        </div>
      ))}
    </div>
  );
};

export default QueryResponse;
