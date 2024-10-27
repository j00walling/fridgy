import React from "react";
import Markdown from 'react-markdown';

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
          <p className="font-bold mb-1">You:</p>
          <p className="ml-4">{query.question}</p>
          <p className="font-bold mt-3 mb-1">Fridgy:</p>
          <div className="ml-4">
            <Markdown>{query.response}</Markdown>
          </div>
        </div>
      ))}
    </div>
  );
};

export default QueryResponse;
