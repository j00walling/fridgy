"use client";

import { useState, ChangeEvent } from "react";
import { ArrowUpIcon } from "@heroicons/react/24/outline";
import Loader from "@/app/ui/loader";
import { SearchProps } from "@/app/types/interfaces";
import clsx from "clsx";

export default function Search({
  inputValue,
  setInputValue,
  onSubmit,
}: {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSubmit: (question: string) => Promise<void>;
}) {
  const [loading, setLoading] = useState<boolean>(false);

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async () => {
    if (!inputValue.trim()) return;
    const question = inputValue.trim();

    setLoading(true);
    try {
      await onSubmit(question);
    } catch (error) {
      console.error("Error submitting question:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex flex-1 flex-shrink-0">
      <input
        value={inputValue}
        onChange={handleInputChange}
        disabled={loading}
        className="peer block w-full rounded-md border border-gray-200 py-[9px] pl-3 pr-12 text-sm outline-2 placeholder:text-gray-500 focus:border-gray-400 focus:ring-0"
        placeholder="Ask Fridgy..."
      />
      <button
        onClick={handleSubmit}
        className={clsx(
          "absolute right-2 top-1/2 h-6 w-6 -translate-y-1/2 flex items-center justify-center rounded-full",
          {
            "bg-gray-900 text-white": inputValue,
            "bg-gray-300 text-gray-500": !inputValue,
          },
        )}
        disabled={loading}
      >
        {loading ? <Loader /> : <ArrowUpIcon className="h-4 w-4" />}
      </button>
    </div>
  );
}