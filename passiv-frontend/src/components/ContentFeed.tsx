import React, { useEffect, useState } from 'react';

interface ContentItem {
  id: number;
  version: number;
  content: string;
  opportunity?: {
    ticker: string;
    opportunity_name: string;
  };
}

const ContentFeed: React.FC = () => {
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/`)
      .then((res) => res.json())
      .then((data) => setContentItems(data));
  }, []);

  return (
    <div className="bg-gray-50 min-h-screen py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-10">
          Investment Insights
        </h1>
        {contentItems.length === 0 ? (
          <p className="text-center text-gray-500">No content available.</p>
        ) : (
          contentItems.map((item) => (
            <div
              key={item.id}
              className="bg-white shadow-md rounded-2xl p-6 mb-6 border border-gray-200"
            >
              <h2 className="text-xl font-semibold text-gray-900">
                {item.opportunity?.opportunity_name || 'Untitled'}{' '}
                <span className="text-sm text-gray-500">
                  ({item.opportunity?.ticker || 'N/A'})
                </span>
              </h2>
              <p className="text-sm text-gray-400 mb-4">v{item.version}</p>
              <p className="text-gray-700 line-clamp-4 whitespace-pre-line leading-relaxed text-base">
                {item.content}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ContentFeed;
