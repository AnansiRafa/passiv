import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

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
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/${id}`)
      .then((res) => res.json())
      .then((data) => setContentItem(data))
      .catch((err) => console.error("Failed to fetch detail:", err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <div className="text-center p-8">Loading content...</div>;
  }

  if (!contentItem) {
    return <div className="text-center p-8">Content not found.</div>;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link to="/" className="text-blue-600 hover:underline mb-4 inline-block">
        ← Back to Feed
      </Link>
      <h1 className="text-3xl font-bold mb-2">{contentItem.opportunity_name || "Untitled"}</h1>
      <div className="text-sm text-gray-500 mb-4">
        Version: v{contentItem.version} • {new Date(contentItem.timestamp).toLocaleDateString()}
      </div>
      <div className="prose dark:prose-invert max-w-none">
        {contentItem.content ? (
          contentItem.content.split("\n").map((line, index) => <p key={index}>{line}</p>)
        ) : (
          <p>No content available.</p>
        )}
      </div>
    </div>
  );
};

export default ContentDetail;
