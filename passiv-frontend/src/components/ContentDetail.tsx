import React from 'react';

interface ContentDetailProps {
  title: string;
  version: number;
  body: string;
}

const ContentDetail: React.FC<ContentDetailProps> = ({ title, version, body }) => {
  return (
    <div className="bg-white shadow-lg rounded-2xl p-8 max-w-4xl mx-auto mt-12 border border-gray-200">
      <h2 className="text-2xl font-bold text-gray-900 mb-1">{title}</h2>
      <p className="text-sm text-gray-500 mb-6">Version {version}</p>
      <article className="prose max-w-none prose-gray">{body}</article>
    </div>
  );
};

export default ContentDetail;
