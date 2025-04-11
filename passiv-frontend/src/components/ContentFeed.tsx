// src/components/ContentFeed.tsx
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

interface ContentItem {
  id: number;
  version: number;
  timestamp: string;
  opportunity_name?: string;
  content?: string;
}

const ContentFeed = (): JSX.Element => {
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/`)
      .then((res) => res.json())
      .then((data) => setContentItems(data))
      .catch((error) => console.error('Failed to fetch content:', error))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-48">
        <span className="text-gray-500 text-lg">Loading...</span>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-6 flex items-center justify-center gap-2">
        <span role="img" aria-label="books">
          📚
        </span>
        Investment Insights
      </h1>

      <div className="space-y-6">
        {contentItems.map((item) => (
          <div
            key={item.id}
            className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow duration-200"
          >
            <Link
              to={`/content/${item.id}`}
              className="text-xl font-semibold text-blue-700 hover:underline"
            >
              {item.opportunity_name || 'Untitled'}
            </Link>

            <div className="text-sm text-gray-500 mt-1">
              v{item.version} • {new Date(item.timestamp).toLocaleDateString()}
            </div>

            <div className="prose prose-sm text-gray-700 mt-4 line-clamp-4">
              <ReactMarkdown>
                {item.content?.slice(0, 280) + '...'}
              </ReactMarkdown>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContentFeed;
