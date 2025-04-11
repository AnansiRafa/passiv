import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

interface ContentItem {
  id: number;
  title: string;
  version: string;
  created_at: string;
  content: string;
}

const ContentFeed = () => {
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/`)
      .then((res) => res.json())
      .then((data) => setContentItems(data));
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6 text-center flex items-center justify-center gap-2">
        <span role="img" aria-label="books">📚</span> Investment Insights
      </h1>

      <div className="space-y-6">
        {contentItems.map((item) => (
          <div
            key={item.id}
            className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 p-6"
          >
            <Link
              to={`/content/${item.id}`}
              className="text-xl font-semibold text-blue-700 hover:underline block"
            >
              {item.title || 'Untitled'}
            </Link>

            <div className="text-sm text-gray-500 mt-1">
              v{item.version || '1'} • {new Date(item.created_at).toLocaleDateString()}
            </div>

            <div className="prose prose-sm text-gray-700 mt-4 line-clamp-4">
              <ReactMarkdown>
                {item.content?.slice(0, 480) + '...'}
              </ReactMarkdown>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContentFeed;
