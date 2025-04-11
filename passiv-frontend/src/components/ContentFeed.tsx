// src/components/ContentFeed.tsx
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ContentItem } from '../types';
import ReactMarkdown from 'react-markdown';


const ContentFeed = (): JSX.Element => {
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/`)
      .then(res => res.json())
      .then(setContentItems)
      .catch(err => setError('Failed to load content.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-center text-gray-500 p-8">Loading content...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 p-8">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-8">📚 Investment Insights</h1>
      <div className="grid gap-6">
        {contentItems.map(item => (
          <Link to={`/content/${item.id}`} key={item.id}>
            <div className="p-6 border border-gray-300 rounded-md shadow hover:shadow-lg transition">
              <h2 className="text-xl font-semibold text-blue-700 hover:underline">
                {item.opportunity_name || 'Untitled'}
              </h2>
              <p className="text-sm text-gray-500 mt-1">
                v{item.version} • {new Date(item.timestamp).toLocaleDateString()}
              </p>
              <div className="prose prose-sm text-gray-700 mt-2 line-clamp-3">
                <ReactMarkdown>
                    {item.content?.slice(0, 280) + '...'}
                </ReactMarkdown>
            </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default ContentFeed;
