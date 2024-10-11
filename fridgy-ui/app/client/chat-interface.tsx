"use client";

import { useState } from "react";
import Search from "@/app/ui/search";
import QueryResponse from "@/app/ui/query-response";
import Sidebar from "@/app/ui/sidebar";
import { Query } from "@/app/types/interfaces";

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [queries, setQueries] = useState<Query[]>([]);

  return (
    <main className="flex min-h-screen p-6">
      <Sidebar setInputValue={setInputValue} />
      <div className="flex-grow flex flex-col justify-between ml-4">
        <div className="text-black text-center py-4 rounded-md mb-6">
          <h1 className="text-4xl">Welcome to Fridgy!</h1>
          <p className="mt-3">
            Your artificially intelligent refrigerator assistant
          </p>
        </div>
        <div className="flex-grow">
          <QueryResponse queries={queries} />
        </div>
        <div className="relative w-[50%] mx-auto mb-5">
          <Search
            inputValue={inputValue}
            setInputValue={setInputValue}
            setQueries={setQueries}
          />
        </div>
      </div>
    </main>
  );
};

export default ChatInterface;
