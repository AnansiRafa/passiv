// src/components/ContentDetail.tsx
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ContentItem } from '../types';
import ReactMarkdown from 'react-markdown';

const ContentDetail = (): JSX.Element => {
  const { id } = useParams();
  const [contentItem, setContentItem] = useState<ContentItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/${id}/`)
      .then(res => res.json())
      .then(setContentItem)
      .catch(err => setError('Failed to load content.'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <div className="text-center text-gray-500 p-8">Loading details...</div>;
  }

  if (error || !contentItem) {
    return <div className="text-center text-red-500 p-8">{error || 'Content not found.'}</div>;
  }

  return (
    <div className="max-w-3xl mx-auto p-4">
      <Link to="/" className="text-blue-600 hover:underline text-sm">&larr; Back to all insights</Link>
      <h1 className="text-3xl font-bold mt-4 mb-2">{contentItem.opportunity_name || 'Untitled'}</h1>
      <p className="text-sm text-gray-500 mb-6">
        Version {contentItem.version} • {new Date(contentItem.timestamp).toLocaleDateString()}
      </p>
      <div className="prose prose-neutral prose-lg">
        <ReactMarkdown>{contentItem.content || 'No content available.'}</ReactMarkdown>
      </div>
    </div>
  );
};

export default ContentDetail;
