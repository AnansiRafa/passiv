import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";

interface ContentItem {
  id: number;
  version: number;
  timestamp: string;
  opportunity_name?: string;
  content?: string;
}

const ContentDetail = (): JSX.Element => {
  const { id } = useParams();
  const [contentItem, setContentItem] = useState<ContentItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/${id}/`)
      .then((res) => res.json())
      .then((data) => {
        setContentItem(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch content detail:", error);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <div className="text-center p-8 text-gray-500">Loading...</div>;
  }

  if (!contentItem) {
    return <div className="text-center p-8 text-red-500">Content not found.</div>;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link to="/" className="text-blue-600 hover:underline text-sm">
        ← Back to Feed
      </Link>
      <h1 className="text-3xl font-bold mt-4">
        {contentItem.opportunity_name || "Untitled"}
      </h1>
      <div className="text-sm text-gray-500 mt-1 mb-4">
        v{contentItem.version} • {new Date(contentItem.timestamp).toLocaleDateString()}
      </div>
      <div className="prose max-w-none text-gray-800">
        <ReactMarkdown>{contentItem.content || ""}</ReactMarkdown>
      </div>
    </div>
  );
};

export default ContentDetail;
