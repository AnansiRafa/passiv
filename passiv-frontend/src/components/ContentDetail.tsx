import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

interface ContentItem {
  id: number;
  title: string;
  version: string;
  timestamp: string;
  content: string;
}

const ContentDetail = () => {
  const { id } = useParams();
  const [contentItem, setContentItem] = useState<ContentItem | null>(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/${id}/`)
      .then((res) => res.json())
      .then((data) => setContentItem(data));
  }, [id]);

  if (!contentItem) {
    return <div className="text-center mt-10 text-gray-600">Loading...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <Link
        to="/"
        className="text-sm text-blue-600 hover:underline mb-6 inline-block"
      >
        ← Back to Feed
      </Link>

      <h1 className="text-3xl font-bold text-center mb-2">
        {contentItem.title || 'Untitled'}
      </h1>

      <div className="text-center text-sm text-gray-500 mb-6">
        v{contentItem.version || '1'} • {contentItem.timestamp
              ? new Date(contentItem.timestamp).toLocaleDateString(): "Unknown Date"}
      </div>

      <article className="prose max-w-none text-gray-800 mx-auto">
        <ReactMarkdown>{contentItem.content}</ReactMarkdown>
      </article>
    </div>
  );
};

export default ContentDetail;
